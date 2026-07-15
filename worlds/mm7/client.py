from __future__ import annotations

import logging
from typing import Dict, Optional

from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient

from . import names
from .items import rom_receive_id
from .locations import location_name_to_id

snes_logger = logging.getLogger("SNES")

# FXPAK Pro / SNI memory mapping.
# See existing SNES/SNI worlds such as Super Mario World.
ROM_START = 0x000000
WRAM_START = 0xF50000

MM7_ROM_HEADER = ROM_START + 0x00FFC0
ROM_HEADER_SIZE = 0x15

# File offset written by rom.py: 0x18FEC0
# SNES HiROM bus address read by SNI: $D8FEC0
MM7_ROM_AUTH_TOKEN = ROM_START + 0xD8FEC0
MM7_ROM_AUTH_TOKEN_SIZE = 32
MM7_ROM_AUTH_TOKEN_PREFIX = b"MM7AP"

# AP runtime/check block in WRAM.
# These must match your ASM symbols.
AP_BOSS_FLAGS = WRAM_START + 0x1FA1
AP_BOSS_FLAGS_2 = WRAM_START + 0x1FA2
AP_DEBUG_FLAGS = WRAM_START + 0x1FA3
AP_ITEM_ID_LO = WRAM_START + 0x1FA4
AP_ITEM_ID_HI = WRAM_START + 0x1FA5
AP_EXECUTE_FLAG = WRAM_START + 0x1FA6
AP_RECV_INDEX_LO = WRAM_START + 0x1FA7
AP_RECV_INDEX_HI = WRAM_START + 0x1FA8
AP_CONNECTION = WRAM_START + 0x1FA9
AP_GOAL_FLAGS = WRAM_START + 0x1FAC
AP_PICKUP_FLAGS = WRAM_START + 0x1FB0
AP_MEGA_FLAGS = WRAM_START + 0x1FB2
AP_MISC_FLAGS = WRAM_START + 0x1FB3
AP_WILY_FLAGS = WRAM_START + 0x1FB4

BOSS_FLAG_TO_ITEM_LOCATION: Dict[int, str] = {
    0x01: names.freeze_man_defeated_item,
    0x02: names.cloud_man_defeated_item,
    0x04: names.junk_man_defeated_item,
    0x08: names.turbo_man_defeated_item,
    0x10: names.slash_man_defeated_item,
    0x20: names.shade_man_defeated_item,
    0x40: names.burst_man_defeated_item,
    0x80: names.spring_man_defeated_item,
}

PROTO_FLAG_TO_LOCATION: Dict[int, str] = {
    0x01: names.proto_man_cloud_man_loc,
    0x02: names.proto_man_turbo_man_loc,
    0x04: names.proto_shield_loc,
}

RUSH_FLAG_TO_LOCATION = {
    0x01: names.rush_search_loc,
    0x02: names.rush_jet_loc,
    0x04: names.rush_coil_loc,
}

ITEM_FLAG_TO_LOCATION = {
    0x01: names.rush_r_plate_loc,
    0x02: names.rush_u_plate_loc,
    0x04: names.rush_s_plate_loc,
    0x08: names.rush_h_plate_loc,
    0x10: names.hyper_bolt_loc,
    0x20: names.exit_unit_loc,
    0x40: names.hyper_rocket_buster_loc,
    0x80: names.energy_balancer_loc,
}

MEGA_FLAG_TO_LOCATION = {
    0x01: names.mega_bolt_junk_man_loc,
    0x02: names.mega_bolt_turbo_man_loc,
    0x04: names.mega_bolt_shade_man_loc,
    0x08: names.mega_bolt_cloud_man_loc,
    0x10: names.mega_health_capsule_loc,
    0x20: names.mega_bolt_spring_man_loc,
}

MISC_FLAG_TO_LOCATION = {
    0x01: names.beat_loc,
    0x02: names.mash_defeated,
}

WILY_FLAG_TO_LOCATION = {
    0x01: names.guts_man_g_defeated_item,
    0x02: names.gamerizer_defeated_item,
    0x04: names.hannya_ned_defeated_item,
}

class MM7SNIClient(SNIClient):
    game = "Mega Man 7"
    patch_suffix = ".apmm7"

    async def validate_rom(self, ctx) -> bool:
        from SNIClient import snes_read

        rom_header = await snes_read(ctx, MM7_ROM_HEADER, ROM_HEADER_SIZE)
        if rom_header is None:
            return False

        try:
            title = bytes(rom_header).decode("ascii", errors="ignore").strip()
        except Exception:
            return False

        title_upper = title.upper()
        if "MEGAMAN 7" not in title_upper and "MEGA MAN 7" not in title_upper:
            return False

        auth_token = await snes_read(ctx, MM7_ROM_AUTH_TOKEN, MM7_ROM_AUTH_TOKEN_SIZE)
        if auth_token is None:
            return False

        auth_token = bytes(auth_token)

        if not auth_token.startswith(MM7_ROM_AUTH_TOKEN_PREFIX):
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.rom = auth_token

        return True

    async def game_watcher(self, ctx) -> None:
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        # If we are not connected to an AP room yet, do not try to sync.
        if ctx.server is None or ctx.slot is None:
            return

        # 1. Send boss-defeat location checks from ROM flags.
        boss_flags = await snes_read(ctx, AP_BOSS_FLAGS, 1)
        if boss_flags is None:
            return

        new_checks = []
        flags = boss_flags[0]
        goal_reached = False

        goal_flags = await snes_read(ctx, AP_GOAL_FLAGS, 1)
        if goal_flags and goal_flags[0] & 0x01:
            goal_reached = True

        for bit, location_name in BOSS_FLAG_TO_ITEM_LOCATION.items():
            if not flags & bit:
                continue

            location_id = location_name_to_id.get(location_name)
            if location_id is None:
                snes_logger.warning("MM7 client missing location id for %s", location_name)
                continue

            if location_id not in ctx.locations_checked:
                new_checks.append(location_id)
                
        proto_flags_raw = await snes_read(ctx, AP_BOSS_FLAGS_2, 1)
        if proto_flags_raw is None:
            return

        proto_flags = proto_flags_raw[0]

        for bit, location_name in PROTO_FLAG_TO_LOCATION.items():
            if not proto_flags & bit:
                continue

            location_id = location_name_to_id.get(location_name)
            if location_id is None:
                snes_logger.warning("MM7 client missing location id for %s", location_name)
                continue

            if location_id not in ctx.locations_checked:
                new_checks.append(location_id)

        pickup_flags_raw = await snes_read(ctx, AP_PICKUP_FLAGS, 2)
        if pickup_flags_raw is None:
            return

        rush_flags = pickup_flags_raw[0]
        item_flags = pickup_flags_raw[1]

        for bit, location_name in RUSH_FLAG_TO_LOCATION.items():
            if not rush_flags & bit:
                continue

            location_id = location_name_to_id.get(location_name)
            if location_id is None:
                snes_logger.warning("MM7 client missing location id for %s", location_name)
                continue

            if location_id not in ctx.locations_checked:
                new_checks.append(location_id)

        for bit, location_name in ITEM_FLAG_TO_LOCATION.items():
            if not item_flags & bit:
                continue

            location_id = location_name_to_id.get(location_name)
            if location_id is None:
                snes_logger.warning("MM7 client missing location id for %s", location_name)
                continue

            if location_id not in ctx.locations_checked:
                new_checks.append(location_id)

        mega_flags_raw = await snes_read(ctx, AP_MEGA_FLAGS, 1)
        if mega_flags_raw is None:
            return

        mega_flags = mega_flags_raw[0]

        for bit, location_name in MEGA_FLAG_TO_LOCATION.items():
            if not mega_flags & bit:
                continue

            location_id = location_name_to_id.get(location_name)
            if location_id is None:
                snes_logger.warning("MM7 client missing location id for %s", location_name)
                continue

            if location_id not in ctx.locations_checked:
                new_checks.append(location_id)

        misc_flags_raw = await snes_read(ctx, AP_MISC_FLAGS, 1)
        if misc_flags_raw is None:
            return

        misc_flags = misc_flags_raw[0]

        for bit, location_name in MISC_FLAG_TO_LOCATION.items():
            if not misc_flags & bit:
                continue

            location_id = location_name_to_id.get(location_name)
            if location_id is None:
                snes_logger.warning("MM7 client missing location id for %s", location_name)
                continue

            if location_id not in ctx.locations_checked:
                new_checks.append(location_id)

        wily_flags = await snes_read(ctx, AP_WILY_FLAGS, 1)
        if wily_flags is None:
            return

        flags = wily_flags[0]

        for bit, location_name in WILY_FLAG_TO_LOCATION.items():
            if not flags & bit:
                continue

            location_id = location_name_to_id.get(location_name)
            if location_id is None:
                snes_logger.warning("MM7 client missing location id for %s", location_name)
                continue

            if location_id not in ctx.locations_checked:
                new_checks.append(location_id)

        if new_checks:
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": new_checks}])
            for location_id in new_checks:
                ctx.locations_checked.add(location_id)

        if goal_reached and not ctx.finished_game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

        # 2. Deliver received AP items to the ROM-side AP_CheckItemReceive mailbox.
        execute_flag = await snes_read(ctx, AP_EXECUTE_FLAG, 1)
        recv_index_raw = await snes_read(ctx, AP_RECV_INDEX_LO, 2)
        if execute_flag is None or recv_index_raw is None:
            return

        # Wait until the ROM has consumed the previous item.
        if execute_flag[0] != 0:
            return

        recv_index = recv_index_raw[0] | (recv_index_raw[1] << 8)
        if recv_index >= len(ctx.items_received):
            return

        network_item = ctx.items_received[recv_index]

        try:
            item_name: Optional[str] = ctx.item_names.lookup_in_game(network_item.item)
        except Exception:
            # This should not normally happen, but do not crash the client if
            # the item lookup table is incomplete during early development.
            snes_logger.warning("Could not resolve received item id %s", network_item.item)
            return

        receive_id = rom_receive_id.get(item_name)
        if receive_id is None:
            snes_logger.warning("No MM7 ROM receive id for item: %s", item_name)
            return

        sending_player = ctx.player_names.get(network_item.player, f"Player {network_item.player}")
        location_text = ctx.location_names.lookup_in_slot(network_item.location, network_item.player)

        snes_logger.info(
            "Received %s from %s at %s (%d/%d)",
            color(item_name, "red", "bold"),
            color(sending_player, "yellow"),
            location_text,
            recv_index + 1,
            len(ctx.items_received),
        )

        snes_buffered_write(ctx, AP_ITEM_ID_LO, bytes([receive_id & 0xFF]))
        snes_buffered_write(ctx, AP_ITEM_ID_HI, bytes([(receive_id >> 8) & 0xFF]))
        snes_buffered_write(ctx, AP_EXECUTE_FLAG, bytes([0x01]))
        await snes_flush_writes(ctx)