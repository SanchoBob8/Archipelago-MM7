# worlds/mm7/__init__.py

from __future__ import annotations

import base64
import os
from typing import Any, Dict, List

from BaseClasses import ItemClassification, Region, Tutorial
from worlds.AutoWorld import WebWorld, World

from . import names
from .items import (
    MM7Item,
    item_groups,
    item_name_to_id,
    create_item as create_mm7_item,
    get_filler_item_name as get_mm7_filler_item_name,
)

from .locations import (
    MM7Location,
    active_locations,
    event_location_to_item,
    location_name_to_id,
)

from .options import MegaMan7Options
from .rom import MM7ProcedurePatch, MM7Settings, patch_rom, get_rom_auth_token
from .client import MM7SNIClient
from .rules import set_rules as set_mm7_rules


class MegaMan7WebWorld(WebWorld):
    theme = "stone"
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


# One randomized item per active non-event location.
ITEM_POOL: List[str] = [
    # Weapons
    names.freeze_cracker,
    names.danger_wrap,
    names.thunder_bolt,
    names.junk_shield,
    names.slash_claw,
    names.wild_coil,
    names.noise_crush,
    names.scorch_wheel,

    # Randomized Proto Man clue/items
    names.proto_man_cloud_man,
    names.proto_man_turbo_man,
    names.proto_shield,

    # Rush items
    names.rush_search,
    names.rush_jet,
    names.rush_coil,

    # Rush plates and unique upgrades
    names.rush_r_plate,
    names.rush_u_plate,
    names.rush_s_plate,
    names.rush_h_plate,
    names.hyper_bolt,
    names.exit_unit,
    names.hyper_rocket_buster,
    names.energy_balancer,
    names.beat,

    # Wily access codes
    names.wily_1_access,
    names.wily_2_access,
    names.wily_3_access,

    # Fillers
    names.one_up,
    names.one_up,
    names.e_tank,
    names.e_tank,
    names.w_tank,
    names.w_tank,
    names.s_tank,
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

    location_name_to_id = location_name_to_id

    # Use the canonical AP item ids from items.py.
    # items.py correctly adds MM7_ITEM_ID_BASE and excludes event items.
    item_name_to_id = item_name_to_id
    item_name_groups = item_groups

    def create_item(self, name: str) -> MM7Item:
        return create_mm7_item(name, self.player)

    def create_event(self, name: str) -> MM7Item:
        return MM7Item(name, ItemClassification.progression, None, self.player)

    def create_items(self) -> None:
        self.multiworld.itempool += [
            self.create_item(item_name)
            for item_name in ITEM_POOL
        ]

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)
        main_stages = Region("Main Stages", self.player, self.multiworld)

        menu.connect(main_stages)

        for location_name in active_locations:
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

    def modify_multidata(self, multidata: Dict[str, Any]) -> None:
        auth_name = base64.b64encode(get_rom_auth_token(self)).decode()
        player_name = self.multiworld.player_name[self.player]
        multidata["connect_names"][auth_name] = multidata["connect_names"][player_name]

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "minimal": True,
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
