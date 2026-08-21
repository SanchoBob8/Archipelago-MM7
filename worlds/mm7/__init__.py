# worlds/mm7/__init__.py

from __future__ import annotations

import base64
import os
from typing import Any, Dict, Optional

from BaseClasses import (
    Item,
    ItemClassification,
    Location,
    Region,
    Tutorial,
)
from worlds.AutoWorld import WebWorld, World

from . import names
from .items import (
    MM7Item,
    create_item as create_mm7_item,
    get_filler_item_name as get_mm7_filler_item_name,
    get_pool_items,
    item_groups,
    item_name_to_id,
    robot_master_access_codes,
)

from .locations import (
    MM7Location,
    active_locations,
    pickupsanity_locations,
    event_location_to_item,
    location_name_to_id,
)

from .options import MegaMan7Options, mm7_option_groups
from .rom import MM7ProcedurePatch, MM7Settings, patch_rom, get_rom_auth_token
from .client import MM7SNIClient
from .rules import (
    BOSS_ITEM_LOCATION_TABLE,
    ROBOT_MASTER_ACCESS_CODE_TABLE,
    WEAKNESS_TABLE,
    set_rules as set_mm7_rules,
)


class MegaMan7WebWorld(WebWorld):
    theme = "stone"
    option_groups = mm7_option_groups

    tutorials = [
        Tutorial(
            tutorial_name="Setup Guide",
            description="A guide to setting up Mega Man 7 for Archipelago.",
            language="English",
            file_name="setup_en.md",
            link="setup/en",
            authors=["SanchoBob"],
        )
    ]

class MegaMan7World(World):
    """Mega Man 7 for Archipelago.

    Randomizes Robot Master rewards, major upgrades, Rush items, Proto Man checks,
    Wily access codes, and selected stage pickups.
    """

    game = "Mega Man 7"
    web = MegaMan7WebWorld()

    options_dataclass = MegaMan7Options
    options: MegaMan7Options

    settings: MM7Settings
    settings_key = "mm7_options"

    starting_robot_master: Optional[str]
    starting_robot_master_access_code: Optional[str]
    starting_robot_master_weakness: Optional[str]

    location_name_to_id = location_name_to_id

    # Use the canonical AP item ids from items.py.
    # items.py correctly adds MM7_ITEM_ID_BASE and excludes event items.
    item_name_to_id = item_name_to_id
    item_name_groups = item_groups

    def create_item(self, name: str) -> MM7Item:
        return create_mm7_item(name, self.player)

    def create_event(self, name: str) -> MM7Item:
        return MM7Item(name, ItemClassification.progression, None, self.player)

    def _get_active_location_names(self) -> list[str]:
        location_names = list(active_locations)

        if self.options.pickupsanity.value:
            location_names.extend(pickupsanity_locations)

        return location_names

    def create_items(self) -> None:
        access_codes_enabled = bool(
            self.options.robot_master_access_codes.value
        )

        starter_items: list[str] = []

        if self.starting_robot_master_access_code is not None:
            starter_items.append(
                self.starting_robot_master_access_code
            )

        if self.starting_robot_master_weakness is not None:
            starter_items.append(
                self.starting_robot_master_weakness
            )

        for item_name in starter_items:
            self.multiworld.push_precollected(
                self.create_item(item_name)
            )

        pool = get_pool_items(
            excluded_items=set(starter_items),
            include_robot_master_access_codes=access_codes_enabled,
        )

        # When weakness logic is enabled alongside Access Codes, the matching
        # starting weapon is also precollected. Add one filler to preserve the
        # randomized item/location count.
        if self.starting_robot_master_weakness is not None:
            pool.append(self.get_filler_item_name())

        # Pickupsanity adds 72 randomized locations without adding
        # 72 new progression items, so fill the additional slots
        # using the normal MM7 filler pool.
        if self.options.pickupsanity.value:
            pool.extend(
                self.get_filler_item_name()
                for _ in pickupsanity_locations
            )

        active_location_names = self._get_active_location_names()

        randomized_location_count = sum(
            1
            for location_name in active_location_names
            if location_name in location_name_to_id
        )

        assert len(pool) == randomized_location_count, (
            f"MM7 item pool contains {len(pool)} items, but "
            f"{randomized_location_count} randomized locations exist."
        )

        self.multiworld.itempool += [
            self.create_item(item_name)
            for item_name in pool
        ]

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)
        main_stages = Region("Main Stages", self.player, self.multiworld)

        menu.connect(main_stages)

        for location_name in self._get_active_location_names():
            location_code = self.location_name_to_id.get(location_name)

            location = MM7Location(
                self.player,
                location_name,
                location_code,
                main_stages,
            )

            event_item_name = event_location_to_item.get(location_name)
            if event_item_name is not None:
                location.place_locked_item(self.create_event(event_item_name))

            main_stages.locations.append(location)

        self.multiworld.regions += [menu, main_stages]

    def set_rules(self) -> None:
        set_mm7_rules(self, self.multiworld, self.player)

    def get_filler_item_name(self) -> str:
        return get_mm7_filler_item_name(self)

    def generate_output(self, output_directory: str) -> None:
        patch = MM7ProcedurePatch(
            player=self.player,
            player_name=self.multiworld.player_name[self.player],
        )
        patch_rom(self, patch)
        patch.write(
            os.path.join(
                output_directory,
                f"{self.multiworld.get_out_file_name_base(self.player)}.apmm7",
            )
        )

    def generate_early(self) -> None:
        self.starting_robot_master = None
        self.starting_robot_master_access_code = None
        self.starting_robot_master_weakness = None

        if not self.options.robot_master_access_codes.value:
            return

        self.starting_robot_master = self.random.choice(
            tuple(ROBOT_MASTER_ACCESS_CODE_TABLE)
        )

        self.starting_robot_master_access_code = (
            ROBOT_MASTER_ACCESS_CODE_TABLE[
                self.starting_robot_master
            ]
        )

        if self.options.logic_boss_weakness.value:
            self.starting_robot_master_weakness = self.random.choice(
                WEAKNESS_TABLE[self.starting_robot_master]
            )

    def modify_multidata(self, multidata: Dict[str, Any]) -> None:
        auth_name = base64.b64encode(get_rom_auth_token(self)).decode()
        player_name = self.multiworld.player_name[self.player]
        multidata["connect_names"][auth_name] = multidata["connect_names"][player_name]

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "minimal": True,
            "death_link": bool(self.options.death_link.value),
            "robot_master_access_codes": bool(
                self.options.robot_master_access_codes.value
            ),
            "pickupsanity": bool(self.options.pickupsanity.value),
            "ap_wram_base": 0x1FA1,
            "boss_flag_order": {
                "freeze": 0x01,
                "cloud": 0x02,
                "junk": 0x04,
                "turbo": 0x08,
                "slash": 0x10,
                "shade": 0x20,
                "burst": 0x40,
                "spring": 0x80,
            },
        }

    def fill_hook(
        self,
        progitempool: list[Item],
        usefulitempool: list[Item],
        filleritempool: list[Item],
        fill_locations: list[Location],
    ) -> None:
        if not self.options.robot_master_access_codes.value:
            return

        if not self.options.logic_boss_weakness.value:
            return

        if self.multiworld.players > 1:
            return

        affected_starting_bosses = {
            names.cloud_man_defeated,
            names.slash_man_defeated,
            names.shade_man_defeated,
        }

        if self.starting_robot_master not in affected_starting_bosses:
            return

        starting_weapon = self.starting_robot_master_weakness
        if starting_weapon is None:
            return

        productive_second_bosses = {
            names.burst_man_defeated,
            names.junk_man_defeated,
            names.freeze_man_defeated,
            names.spring_man_defeated,
            names.turbo_man_defeated,
        }

        candidates: list[tuple[str, Item, bool]] = []

        for boss in productive_second_bosses:
            access_code_name = ROBOT_MASTER_ACCESS_CODE_TABLE[boss]

            access_code_item = next(
                (
                    item
                    for item in progitempool
                    if item.player == self.player
                    and item.name == access_code_name
                ),
                None,
            )

            if access_code_item is None:
                continue

            candidates.append(
                (
                    boss,
                    access_code_item,
                    starting_weapon in WEAKNESS_TABLE[boss],
                )
            )

        if not candidates:
            raise RuntimeError(
                "MM7 could not find a productive second Robot Master "
                "Access Code during fill."
            )

        # Prefer a stage that is already weak to the starting weapon.
        shared_weakness_candidates = [
            candidate
            for candidate in candidates
            if candidate[2]
        ]

        second_boss, access_code_item, already_has_weakness = (
            self.random.choice(
                shared_weakness_candidates or candidates
            )
        )

        starting_boss_reward = self.get_location(
            BOSS_ITEM_LOCATION_TABLE[self.starting_robot_master]
        )

        if starting_boss_reward not in fill_locations:
            raise RuntimeError(
                f"MM7 expected {starting_boss_reward.name} to be "
                f"available during fill."
            )

        # Clearing the starting boss unlocks a productive second stage.
        starting_boss_reward.place_locked_item(access_code_item)
        progitempool.remove(access_code_item)
        fill_locations.remove(starting_boss_reward)

        if already_has_weakness:
            return

        valid_weakness_items = [
            item
            for item in progitempool
            if item.player == self.player
            and item.name in WEAKNESS_TABLE[second_boss]
        ]

        if not valid_weakness_items:
            raise RuntimeError(
                f"MM7 could not find a weakness for {second_boss} "
                f"during fill."
            )

        weakness_item = self.random.choice(valid_weakness_items)

        intro_location = self.get_location(names.rush_coil_loc)

        if intro_location not in fill_locations:
            raise RuntimeError(
                f"MM7 expected {intro_location.name} to be "
                f"available during fill."
            )

        # Intro provides the weakness required by the second stage.
        intro_location.place_locked_item(weakness_item)
        progitempool.remove(weakness_item)
        fill_locations.remove(intro_location)
