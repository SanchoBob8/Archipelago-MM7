from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, Optional

from NetUtils import ClientStatus
from Utils import async_start
from worlds.AutoSNIClient import SNIClient

from . import names
from .items import rom_receive_id
from .locations import (
    boss_rush_locations,
    location_name_to_id,
    pickupsanity_locations,
)

snes_logger = logging.getLogger("SNES")

# FXPAK Pro / SNI memory mapping.
# See existing SNES/SNI worlds such as Super Mario World.
ROM_START = 0x000000
WRAM_START = 0xF50000

MM7_HEALTH = WRAM_START + 0x0C2E
MM7_LIVES = WRAM_START + 0x0B81

MM7_PLAYER_STATE = WRAM_START + 0x0BD7
MM7_CONTROL_STATE = WRAM_START + 0x0BC6

MM7_PLAYER_ACTIVE = 0x07
MM7_CONTROLS_ENABLED = 0x00

MM7_ROM_HEADER = ROM_START + 0x00FFC0
ROM_HEADER_SIZE = 0x15

# File offset written by rom.py: 0x18FEC0
# SNES HiROM bus address read by SNI: $D8FEC0
MM7_ROM_AUTH_TOKEN = ROM_START + 0x18FEC0
MM7_ROM_AUTH_TOKEN_SIZE = 32
MM7_ROM_AUTH_TOKEN_PREFIX = b"MM7AP"

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
AP_BOSS_RUSH_FLAGS = WRAM_START + 0x1FCA

# 9 bytes = 72 Pickupsanity locations.
AP_PICKUP_CHECKS = WRAM_START + 0x1FC1
AP_PICKUP_CHECKS_SIZE = 9

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

    def __init__(self) -> None:
        self.previous_health: Optional[int] = None
        self.previous_lives: Optional[int] = None
        self.previous_player_ready = False
        self.pickupsanity_enabled = False
        self.boss_rush_checks_enabled = False

    async def deathlink_kill_player(self, ctx) -> None:
        from SNIClient import (
            DeathState,
            snes_buffered_write,
            snes_flush_writes,
            snes_read,
        )

        health_raw = await snes_read(ctx, MM7_HEALTH, 1)
        player_state_raw = await snes_read(ctx, MM7_PLAYER_STATE, 1)
        control_state_raw = await snes_read(ctx, MM7_CONTROL_STATE, 1)

        if (
            health_raw is None
            or player_state_raw is None
            or control_state_raw is None
        ):
            await asyncio.sleep(0.1)
            return

        health = health_raw[0]
        player_state = player_state_raw[0]
        control_state = control_state_raw[0]

        player_ready = (
            player_state == MM7_PLAYER_ACTIVE
            and control_state == MM7_CONTROLS_ENABLED
            and health > 0
        )

        # Keep the incoming DeathLink pending until Mega Man is alive,
        # inside active gameplay, and accepting player input.
        if not player_ready:
            await asyncio.sleep(0.1)
            return

        snes_buffered_write(ctx, MM7_HEALTH, b"\x00")
        await snes_flush_writes(ctx)

        # Prevent the resulting local death from being sent back.
        ctx.death_state = DeathState.dead

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
        if ctx.rom != auth_token:
            self.previous_health = None
            self.previous_lives = None
            self.previous_player_ready = False
        ctx.rom = auth_token

        return True

    def on_package(self, ctx, cmd: str, args: Dict[str, Any]) -> None:
        if cmd != "Connected":
            return

        self.previous_health = None
        self.previous_lives = None
        self.previous_player_ready = False

        slot_data = args.get("slot_data") or {}

        death_link_enabled = bool(slot_data.get("death_link", False))
        self.pickupsanity_enabled = bool(
            slot_data.get("pickupsanity", False)
        )

        self.boss_rush_checks_enabled = bool(
            slot_data.get("boss_rush_checks", False)
        )

        async_start(
            ctx.update_death_link(death_link_enabled),
            name="Update MM7 DeathLink",
        )

    async def game_watcher(self, ctx) -> None:
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        # If we are not connected to an AP room yet, do not try to sync.
        if ctx.server is None or ctx.slot is None:
            return

        # DeathLink
        if "DeathLink" not in ctx.tags:
            self.previous_health = None
            self.previous_lives = None
            self.previous_player_ready = False
        else:
            health_raw = await snes_read(ctx, MM7_HEALTH, 1)
            lives_raw = await snes_read(ctx, MM7_LIVES, 1)
            player_state_raw = await snes_read(ctx, MM7_PLAYER_STATE, 1)
            control_state_raw = await snes_read(ctx, MM7_CONTROL_STATE, 1)

            if (
                health_raw is None
                or lives_raw is None
                or player_state_raw is None
                or control_state_raw is None
            ):
                return

            current_health = health_raw[0]
            current_lives = lives_raw[0]
            current_player_state = player_state_raw[0]
            current_control_state = control_state_raw[0]

            current_player_ready = (
                current_player_state == MM7_PLAYER_ACTIVE
                and current_control_state == MM7_CONTROLS_ENABLED
                and current_health > 0
            )

            health_dropped_to_zero = (
                self.previous_health is not None
                and self.previous_health > 0
                and current_health == 0
            )

            # Normal deaths decrement the remaining-life counter.
            lost_life = (
                self.previous_lives is not None
                and self.previous_lives > 0
                and current_lives == self.previous_lives - 1
                and current_health == 0
            )

            # With zero remaining lives, the counter cannot decrement again.
            # Detect the health transition while the game still reports the
            # active, control-enabled gameplay state.
            lost_final_life = (
                self.previous_lives == 0
                and current_lives == 0
                and self.previous_player_ready
                and health_dropped_to_zero
                and current_player_state == MM7_PLAYER_ACTIVE
                and current_control_state == MM7_CONTROLS_ENABLED
            )

            if lost_life or lost_final_life:
                player_name = ctx.player_names.get(ctx.slot, "Mega Man")

                await ctx.handle_deathlink_state(
                    True,
                    f"{player_name} was defeated in Mega Man 7.",
                )
            elif current_player_ready:
                await ctx.handle_deathlink_state(False)

            self.previous_health = current_health
            self.previous_lives = current_lives
            self.previous_player_ready = current_player_ready

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

        # Boss Rush rematch checks.
        #
        # $1FCA bit order:
        #   bit 0 -> Freeze Man
        #   bit 1 -> Slash Man
        #   bit 2 -> Junk Man
        #   bit 3 -> Cloud Man
        #   bit 4 -> Turbo Man
        #   bit 5 -> Spring Man
        #   bit 6 -> Shade Man
        #   bit 7 -> Burst Man
        #
        # boss_rush_locations uses this exact same order.
        #
        # The ROM may set these flags outside Split mode as well, so only
        # report them when the generated slot actually contains the checks.
        if self.boss_rush_checks_enabled:
            boss_rush_flags_raw = await snes_read(
                ctx,
                AP_BOSS_RUSH_FLAGS,
                1,
            )

            if boss_rush_flags_raw is None:
                return

            boss_rush_flags = boss_rush_flags_raw[0]

            for bit_index, location_name in enumerate(boss_rush_locations):
                bit_mask = 1 << bit_index

                if not boss_rush_flags & bit_mask:
                    continue

                location_id = location_name_to_id.get(location_name)

                if location_id is None:
                    snes_logger.warning(
                        "MM7 client missing Boss Rush location id for %s",
                        location_name,
                    )
                    continue

                if location_id not in ctx.locations_checked:
                    new_checks.append(location_id)

        # Pickupsanity
        #
        # ROM layout:
        #   $1FC1 bit 0 -> pickup index 0
        #   ...
        #   $1FC9 bit 7 -> pickup index 71
        #
        # pickupsanity_locations uses this exact same 0-71 order.
        if self.pickupsanity_enabled:
            pickupsanity_flags = await snes_read(
                ctx,
                AP_PICKUP_CHECKS,
                AP_PICKUP_CHECKS_SIZE,
            )

            if pickupsanity_flags is None:
                return

            for byte_index, flag_byte in enumerate(pickupsanity_flags):
                for bit_index in range(8):
                    pickup_index = byte_index * 8 + bit_index

                    # Defensive guard in case the Python table and
                    # ROM bitfield ever become different sizes.
                    if pickup_index >= len(pickupsanity_locations):
                        break

                    bit_mask = 1 << bit_index

                    if not flag_byte & bit_mask:
                        continue

                    location_name = pickupsanity_locations[pickup_index]
                    location_id = location_name_to_id.get(location_name)

                    if location_id is None:
                        snes_logger.warning(
                            "MM7 client missing Pickupsanity location id for %s",
                            location_name,
                        )
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

        snes_buffered_write(ctx, AP_ITEM_ID_LO, bytes([receive_id & 0xFF]))
        snes_buffered_write(ctx, AP_ITEM_ID_HI, bytes([(receive_id >> 8) & 0xFF]))
        snes_buffered_write(ctx, AP_EXECUTE_FLAG, bytes([0x01]))
        await snes_flush_writes(ctx)
