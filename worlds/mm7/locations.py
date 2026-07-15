# worlds/mm7/locations.py

from dataclasses import dataclass
from typing import Dict, List, Optional, Set

from BaseClasses import Location
from . import names


MM7_LOCATION_ID_BASE = 0x770100


@dataclass(frozen=True)
class MM7LocationData:
    code: Optional[int]
    region: str


class MM7Location(Location):
    game = "Mega Man 7"


# ============================================================
# Regions
# ============================================================

MENU = "Menu"
INTRO_STAGE = "Intro Stage"
STAGE_SELECT = "Stage Select"
SHOP = "Shop"
BURST_MAN = "Burst Man"
CLOUD_MAN = "Cloud Man"
JUNK_MAN = "Junk Man"
FREEZE_MAN = "Freeze Man"
SLASH_MAN = "Slash Man"
SPRING_MAN = "Spring Man"
SHADE_MAN = "Shade Man"
TURBO_MAN = "Turbo Man"
ROBOT_MUSEUM = "Robot Museum"
WILY_1 = "Wily 1"
WILY_2 = "Wily 2"
WILY_3 = "Wily 3"
WILY_4 = "Wily 4"


# ============================================================
# Location table
# ============================================================

location_table: Dict[str, MM7LocationData] = {
    # ========================================================
    # Main boss defeats — locked event locations
    # ========================================================
    names.freeze_man_defeated: MM7LocationData(None, FREEZE_MAN),
    names.cloud_man_defeated:  MM7LocationData(None, CLOUD_MAN),
    names.junk_man_defeated:   MM7LocationData(None, JUNK_MAN),
    names.turbo_man_defeated:  MM7LocationData(None, TURBO_MAN),
    names.slash_man_defeated:  MM7LocationData(None, SLASH_MAN),
    names.shade_man_defeated:  MM7LocationData(None, SHADE_MAN),
    names.burst_man_defeated:  MM7LocationData(None, BURST_MAN),
    names.spring_man_defeated: MM7LocationData(None, SPRING_MAN),

    # ========================================================
    # Main boss item checks — randomized item locations
    # ========================================================
    names.freeze_man_defeated_item: MM7LocationData(0x08, FREEZE_MAN),
    names.cloud_man_defeated_item:  MM7LocationData(0x09, CLOUD_MAN),
    names.junk_man_defeated_item:   MM7LocationData(0x0A, JUNK_MAN),
    names.turbo_man_defeated_item:  MM7LocationData(0x0B, TURBO_MAN),
    names.slash_man_defeated_item:  MM7LocationData(0x0C, SLASH_MAN),
    names.shade_man_defeated_item:  MM7LocationData(0x0D, SHADE_MAN),
    names.burst_man_defeated_item:  MM7LocationData(0x0E, BURST_MAN),
    names.spring_man_defeated_item: MM7LocationData(0x0F, SPRING_MAN),

    # ========================================================
    # Fortress / midboss checks
    # ========================================================
    names.mash_defeated: MM7LocationData(0x10, ROBOT_MUSEUM),

    # Wily boss defeats — locked event locations
    names.guts_man_g_defeated: MM7LocationData(None, WILY_1),
    names.gamerizer_defeated:  MM7LocationData(None, WILY_2),
    names.hannya_ned_defeated: MM7LocationData(None, WILY_3),

    # Wily boss item checks — randomized item locations
    names.guts_man_g_defeated_item: MM7LocationData(0x32, WILY_1),
    names.gamerizer_defeated_item:  MM7LocationData(0x33, WILY_2),
    names.hannya_ned_defeated_item: MM7LocationData(0x34, WILY_3),

    # ========================================================
    # Proto Man clue meetings and shield check are randomized item locations.
    # ========================================================
    names.proto_man_cloud_man_loc: MM7LocationData(0x14, CLOUD_MAN),
    names.proto_man_turbo_man_loc: MM7LocationData(0x15, TURBO_MAN),
    names.proto_shield_loc:        MM7LocationData(0x16, SHADE_MAN),

    # ========================================================
    # Rush Plates and unique upgrade pickups — 0x0BA4 bitfield
    # ========================================================
    names.rush_r_plate_loc:            MM7LocationData(0x20, BURST_MAN),
    names.rush_u_plate_loc:            MM7LocationData(0x21, CLOUD_MAN),
    names.rush_s_plate_loc:            MM7LocationData(0x22, JUNK_MAN),
    names.rush_h_plate_loc:            MM7LocationData(0x23, FREEZE_MAN),
    names.hyper_bolt_loc:              MM7LocationData(0x24, SPRING_MAN),
    names.exit_unit_loc:               MM7LocationData(0x25, FREEZE_MAN),
    names.hyper_rocket_buster_loc:     MM7LocationData(0x26, TURBO_MAN),
    names.energy_balancer_loc:         MM7LocationData(0x27, SHADE_MAN),
    names.beat_loc:                    MM7LocationData(0x28, SLASH_MAN),

    # ========================================================
    # Rush item pickups
    # ========================================================
    names.rush_coil_loc:   MM7LocationData(0x29, INTRO_STAGE),
    names.rush_search_loc: MM7LocationData(0x2A, FREEZE_MAN),
    names.rush_jet_loc:    MM7LocationData(0x2B, JUNK_MAN),

    # ========================================================
    # Mega Bolts and Mega Health Capsule — 0x0BB1 bitfield
    # ========================================================
    names.mega_bolt_cloud_man_loc:   MM7LocationData(0x2C, CLOUD_MAN),
    names.mega_bolt_spring_man_loc:  MM7LocationData(0x2D, SPRING_MAN),
    names.mega_bolt_shade_man_loc:   MM7LocationData(0x2E, SHADE_MAN),
    names.mega_bolt_turbo_man_loc:   MM7LocationData(0x2F, TURBO_MAN),
    names.mega_bolt_junk_man_loc:    MM7LocationData(0x30, JUNK_MAN),
    names.mega_health_capsule_loc:   MM7LocationData(0x31, SPRING_MAN),

    # ========================================================
    # Goal
    # ========================================================
    names.wily_capsule: MM7LocationData(None, WILY_4),
}


# ============================================================
# Derived tables
# ============================================================

minimal_boss_locations = [
    names.freeze_man_defeated,
    names.cloud_man_defeated,
    names.junk_man_defeated,
    names.turbo_man_defeated,
    names.slash_man_defeated,
    names.shade_man_defeated,
    names.burst_man_defeated,
    names.spring_man_defeated,
]

boss_item_locations = [
    names.freeze_man_defeated_item,
    names.cloud_man_defeated_item,
    names.junk_man_defeated_item,
    names.turbo_man_defeated_item,
    names.slash_man_defeated_item,
    names.shade_man_defeated_item,
    names.burst_man_defeated_item,
    names.spring_man_defeated_item,
]

proto_man_check_locations = [
    names.proto_man_cloud_man_loc,
    names.proto_man_turbo_man_loc,
    names.proto_shield_loc,
]

rush_check_locations = [
    names.rush_search_loc,
    names.rush_jet_loc,
    names.rush_coil_loc
]

item_bitmap_check_locations = [
    names.rush_r_plate_loc,
    names.rush_u_plate_loc,
    names.rush_s_plate_loc,
    names.rush_h_plate_loc,
    names.hyper_bolt_loc,
    names.exit_unit_loc,
    names.hyper_rocket_buster_loc,
    names.energy_balancer_loc,
]

mega_check_locations = [
    names.mega_bolt_junk_man_loc,
    names.mega_bolt_turbo_man_loc,
    names.mega_bolt_shade_man_loc,
    names.mega_bolt_cloud_man_loc,
    names.mega_health_capsule_loc,
    names.mega_bolt_spring_man_loc,
]

misc_check_locations = [
    names.beat_loc,
    names.mash_defeated
]

wily_boss_event_locations = [
    names.guts_man_g_defeated,
    names.gamerizer_defeated,
    names.hannya_ned_defeated,
]

wily_boss_item_locations = [
    names.guts_man_g_defeated_item,
    names.gamerizer_defeated_item,
    names.hannya_ned_defeated_item,
]

active_locations = (
    minimal_boss_locations
    + boss_item_locations
    + proto_man_check_locations
    + rush_check_locations
    + item_bitmap_check_locations
    + mega_check_locations
    + misc_check_locations
    + wily_boss_event_locations
    + wily_boss_item_locations
    + [names.wily_capsule]
)


location_name_to_id: Dict[str, int] = {
    location_name: MM7_LOCATION_ID_BASE + data.code
    for location_name, data in location_table.items()
    if data.code is not None
}

location_id_to_name: Dict[int, str] = {
    location_id: location_name
    for location_name, location_id in location_name_to_id.items()
}

location_name_to_region: Dict[str, str] = {
    location_name: data.region
    for location_name, data in location_table.items()
}

regions: Set[str] = {
    data.region
    for data in location_table.values()
} | {MENU, STAGE_SELECT, SHOP}


# ============================================================
# Event locations
# ============================================================
# Values are item names from items.py that should be created as locked events.

event_location_to_item: Dict[str, str] = {
    names.freeze_man_defeated: names.freeze_man_defeated,
    names.cloud_man_defeated: names.cloud_man_defeated,
    names.junk_man_defeated: names.junk_man_defeated,
    names.turbo_man_defeated: names.turbo_man_defeated,
    names.slash_man_defeated: names.slash_man_defeated,
    names.shade_man_defeated: names.shade_man_defeated,
    names.burst_man_defeated: names.burst_man_defeated,
    names.spring_man_defeated: names.spring_man_defeated,

    names.guts_man_g_defeated: names.guts_man_g_defeated,
    names.gamerizer_defeated: names.gamerizer_defeated,
    names.hannya_ned_defeated: names.hannya_ned_defeated,

    names.wily_capsule: names.wily_capsule,
}
event_locations: Set[str] = set(event_location_to_item.keys())


# ============================================================
# Location groups
# ============================================================

main_boss_locations: Set[str] = {
    names.burst_man_defeated,
    names.cloud_man_defeated,
    names.junk_man_defeated,
    names.freeze_man_defeated,
    names.slash_man_defeated,
    names.spring_man_defeated,
    names.shade_man_defeated,
    names.turbo_man_defeated,
}

main_boss_item_locations: Set[str] = {
    names.burst_man_defeated_item,
    names.cloud_man_defeated_item,
    names.junk_man_defeated_item,
    names.freeze_man_defeated_item,
    names.slash_man_defeated_item,
    names.spring_man_defeated_item,
    names.shade_man_defeated_item,
    names.turbo_man_defeated_item,
}

fortress_boss_event_locations: Set[str] = {
    names.guts_man_g_defeated,
    names.gamerizer_defeated,
    names.hannya_ned_defeated,
}

fortress_boss_item_locations: Set[str] = {
    names.mash_defeated,
    names.guts_man_g_defeated_item,
    names.gamerizer_defeated_item,
    names.hannya_ned_defeated_item,
}

goal_locations: Set[str] = {
    names.wily_capsule,
}

proto_man_locations: Set[str] = {
    names.proto_man_cloud_man_loc,
    names.proto_man_turbo_man_loc,
    names.proto_shield_loc,
}

rush_plate_locations: Set[str] = {
    names.rush_r_plate_loc,
    names.rush_u_plate_loc,
    names.rush_s_plate_loc,
    names.rush_h_plate_loc,
}

unique_upgrade_locations: Set[str] = {
    names.hyper_bolt_loc,
    names.exit_unit_loc,
    names.hyper_rocket_buster_loc,
    names.energy_balancer_loc,
    names.beat_loc,
    names.proto_shield_loc,
}

rush_item_locations: Set[str] = {
    names.rush_coil_loc,
    names.rush_search_loc,
    names.rush_jet_loc,
}

mega_items_locations: Set[str] = {
    names.mega_bolt_junk_man_loc,
    names.mega_bolt_turbo_man_loc,
    names.mega_bolt_shade_man_loc,
    names.mega_bolt_cloud_man_loc,
    names.mega_health_capsule_loc,
    names.mega_bolt_spring_man_loc,
}

wily_boss_item_location_set: Set[str] = {
    names.guts_man_g_defeated_item,
    names.gamerizer_defeated_item,
    names.hannya_ned_defeated_item,
}

item_name_groups: Dict[str, Set[str]] = {
    "Boss Defeats": main_boss_locations | fortress_boss_event_locations,
    "Boss Items": main_boss_item_locations | fortress_boss_item_locations,
    "Proto Man": proto_man_locations,
    "Rush Plates": rush_plate_locations,
    "Rush Items": rush_item_locations,
    "Unique Upgrades": unique_upgrade_locations,
    "Mega Items": mega_items_locations,
    "Goal": goal_locations,
}


# ============================================================
# Helpers
# ============================================================

def get_locations_for_region(region: str) -> List[str]:
    return [
        location_name
        for location_name, data in location_table.items()
        if data.region == region
    ]


def get_randomizable_locations() -> List[str]:
    return [
        location_name
        for location_name, data in location_table.items()
        if data.code is not None
    ]


def get_event_locations() -> List[str]:
    return list(event_locations)
