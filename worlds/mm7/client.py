from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, Optional

from NetUtils import ClientStatus
from Utils import async_start
from worlds.AutoSNIClient import SNIClient

from . import names
from .items import rom_receive_id
from .locations import location_name_to_id

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

MM7_GAME_STATE = WRAM_START + 0x0034
MM7_STATE_STAGE_SELECT = 0x0132
MM7_STATE_STAGE = 0x0138

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

AP_NOTIFICATION_REQUEST = WRAM_START + 0x1FBF
AP_NOTIFICATION_TIMER = WRAM_START + 0x1FC0
AP_NOTIFICATION_INDEX_LO = WRAM_START + 0x1FC1
AP_NOTIFICATION_INDEX_HI = WRAM_START + 0x1FC2

# $7F7840 = $17840 bytes after $7E0000.
AP_NOTIFICATION_BUFFER = WRAM_START + 0x17840
AP_NOTIFICATION_BUFFER_SIZE = 0x50
AP_NOTIFICATION_HEADER = bytes([
    0x02, 0x02, 0x03, 0x00,
    0x02, 0x10, 0x20, 0x0A,
    0xC6, 0x00, 0x01, 0x20,
    0x0E, 0x08,
])

AP_NOTIFICATION_END = bytes([
    0x07, 0x3C,
    0x05, 0x06,
    0x0B, 0x00,
])

AP_NOTIFICATION_LINE_LENGTH = 22


def sanitize_notification_line(text: str) -> str:
    text = text.upper()

    # Characters currently supported by the opaque stage-select font.
    allowed = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ?-.!'"

    sanitized = "".join(
        character if character in allowed else "?"
        for character in text
    )

    return sanitized[:AP_NOTIFICATION_LINE_LENGTH]

def get_notification_source_line(ctx, network_item) -> str:
    # Archipelago represents precollected/start-inventory items as:
    #   location = -2
    #   player   = 0
    if network_item.location == -2 and network_item.player == 0:
        return "STARTING ITEM"

    # Item found in this player's own world.
    if network_item.player == ctx.slot:
        return "FROM YOUR WORLD"

    # Item found by another player.
    player_name = ctx.player_names.get(
        network_item.player,
        "ARCHIPELAGO",
    )

    return f"FROM {player_name}"

def build_notification_payload(item_name: str, source_line: str) -> bytes:
    item_line = sanitize_notification_line(item_name)
    source_line = sanitize_notification_line(source_line)

    script = (
        AP_NOTIFICATION_HEADER
        + item_line.encode("ascii")
        + bytes([0x08])
        + source_line.encode("ascii")
        + AP_NOTIFICATION_END
    )

    return script.ljust(AP_NOTIFICATION_BUFFER_SIZE, b"\x00")

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

        if new_checks:
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": new_checks}])
            for location_id in new_checks:
                ctx.locations_checked.add(location_id)

        if goal_reached and not ctx.finished_game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

        # 2. Display pending received-item notifications.
        #
        # Item delivery and notification display use separate indices:
        #
        #   AP_RECV_INDEX
        #       Number of received AP items already granted by the ROM.
        #
        #   AP_NOTIFICATION_INDEX
        #       Number of granted items whose notification has finished displaying.
        #
        # Stage select and active gameplay use different notification renderers.
        game_state_raw = await snes_read(ctx, MM7_GAME_STATE, 2)
        notification_state_raw = await snes_read(ctx, AP_NOTIFICATION_REQUEST, 2)
        notification_index_raw = await snes_read(ctx, AP_NOTIFICATION_INDEX_LO, 2)
        notification_recv_index_raw = await snes_read(ctx, AP_RECV_INDEX_LO, 2)

        notification_health_raw = await snes_read(ctx, MM7_HEALTH, 1)
        notification_player_state_raw = await snes_read(ctx, MM7_PLAYER_STATE, 1)
        notification_control_state_raw = await snes_read(ctx, MM7_CONTROL_STATE, 1)

        if (
            game_state_raw is not None
            and notification_state_raw is not None
            and notification_index_raw is not None
            and notification_recv_index_raw is not None
            and notification_health_raw is not None
            and notification_player_state_raw is not None
            and notification_control_state_raw is not None
        ):
            game_state = game_state_raw[0] | (game_state_raw[1] << 8)

            notification_request = notification_state_raw[0]
            notification_timer = notification_state_raw[1]

            notification_index = (
                notification_index_raw[0]
                | (notification_index_raw[1] << 8)
            )

            notification_recv_index = (
                notification_recv_index_raw[0]
                | (notification_recv_index_raw[1] << 8)
            )

            notification_pending = (
                notification_index < notification_recv_index
                and notification_index < len(ctx.items_received)
            )

            notification_request_idle = notification_request == 0

            gameplay_ready = (
                game_state == MM7_STATE_STAGE
                and notification_player_state_raw[0] == MM7_PLAYER_ACTIVE
                and notification_control_state_raw[0] == MM7_CONTROLS_ENABLED
                and notification_health_raw[0] > 0
            )

            if notification_pending and notification_request_idle:
                next_notification_request = None
                clear_notification_timer = False

                if (
                    game_state == MM7_STATE_STAGE_SELECT
                    and notification_timer == 0
                ):
                    # BG3 stage-select renderer.
                    next_notification_request = 0x01

                elif gameplay_ready:
                    # Native gameplay dialogue renderer.
                    next_notification_request = 0x03

                    # If we left stage select before its notification timer
                    # finished, abandon that old display timer. The same pending
                    # notification will now be shown through the gameplay renderer.
                    clear_notification_timer = notification_timer != 0

                if next_notification_request is not None:
                    notification_item = ctx.items_received[notification_index]

                    try:
                        notification_item_name = ctx.item_names.lookup_in_game(
                            notification_item.item
                        )
                    except Exception:
                        snes_logger.warning(
                            "Could not resolve notification item id %s",
                            notification_item.item,
                        )
                        return

                    source_line = get_notification_source_line(
                        ctx,
                        notification_item,
                    )

                    notification_payload = build_notification_payload(
                        notification_item_name,
                        source_line,
                    )

                    if clear_notification_timer:
                        snes_buffered_write(
                            ctx,
                            AP_NOTIFICATION_TIMER,
                            b"\x00",
                        )

                    # Always write a fresh copy because $7F7840 can be
                    # overwritten during transitions.
                    snes_buffered_write(
                        ctx,
                        AP_NOTIFICATION_BUFFER,
                        notification_payload,
                    )

                    # Set REQUEST last.
                    snes_buffered_write(
                        ctx,
                        AP_NOTIFICATION_REQUEST,
                        bytes([next_notification_request]),
                    )

                    await snes_flush_writes(ctx)

        # 3. Deliver received AP items to the ROM-side AP_CheckItemReceive mailbox.
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