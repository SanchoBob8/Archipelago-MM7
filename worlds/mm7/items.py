# worlds/mm7/items.py

from dataclasses import dataclass
from typing import Dict, List, Optional, Set

from BaseClasses import Item, ItemClassification
from . import names


MM7_ITEM_ID_BASE = 0x770000


@dataclass(frozen=True)
class MM7ItemData:
    code: Optional[int]
    classification: ItemClassification
    count: int = 1


class MM7Item(Item):
    game = "Mega Man 7"


# ============================================================
# Item table
# ============================================================

item_table: Dict[str, MM7ItemData] = {
    # ========================================================
    # Weapons
    # ========================================================
    names.freeze_cracker: MM7ItemData(0x00, ItemClassification.progression),
    names.danger_wrap: MM7ItemData(0x01, ItemClassification.progression),
    names.thunder_bolt: MM7ItemData(0x02, ItemClassification.progression),
    names.junk_shield: MM7ItemData(0x03, ItemClassification.progression),
    names.slash_claw: MM7ItemData(0x04, ItemClassification.progression),
    names.wild_coil: MM7ItemData(0x05, ItemClassification.progression),
    names.noise_crush: MM7ItemData(0x06, ItemClassification.progression),
    names.scorch_wheel: MM7ItemData(0x07, ItemClassification.progression),

    # ========================================================
    # Rush items
    # ========================================================
    names.rush_coil: MM7ItemData(0x08, ItemClassification.progression),
    names.rush_search: MM7ItemData(0x09, ItemClassification.progression),
    names.rush_jet: MM7ItemData(0x0A, ItemClassification.progression),

    # ========================================================
    # Rush Plates
    # ========================================================
    names.rush_r_plate: MM7ItemData(0x0B, ItemClassification.progression),
    names.rush_u_plate: MM7ItemData(0x0C, ItemClassification.progression),
    names.rush_s_plate: MM7ItemData(0x0D, ItemClassification.progression),
    names.rush_h_plate: MM7ItemData(0x0E, ItemClassification.progression),

    # ========================================================
    # Upgrades / useful items
    # ========================================================
    names.proto_shield: MM7ItemData(0x0F, ItemClassification.useful),
    names.hyper_bolt: MM7ItemData(0x10, ItemClassification.useful),
    names.exit_unit: MM7ItemData(0x11, ItemClassification.useful),
    names.hyper_rocket_buster: MM7ItemData(0x12, ItemClassification.useful),
    names.energy_balancer: MM7ItemData(0x13, ItemClassification.useful),
    names.beat: MM7ItemData(0x14, ItemClassification.useful),

    # ========================================================
    # Protoman Clues
    # ========================================================
    names.proto_man_cloud_man: MM7ItemData(0x15, ItemClassification.progression),
    names.proto_man_turbo_man: MM7ItemData(0x16, ItemClassification.progression),

    # ========================================================
    # Wily Access Codes
    # ========================================================
    names.wily_1_access: MM7ItemData(0x2D, ItemClassification.progression),
    names.wily_2_access: MM7ItemData(0x2E, ItemClassification.progression),
    names.wily_3_access: MM7ItemData(0x2F, ItemClassification.progression),

    # ========================================================
    # Event items — locked at event locations
    # ========================================================
    names.burst_man_defeated: MM7ItemData(None, ItemClassification.progression),
    names.cloud_man_defeated: MM7ItemData(None, ItemClassification.progression),
    names.junk_man_defeated: MM7ItemData(None, ItemClassification.progression),
    names.freeze_man_defeated: MM7ItemData(None, ItemClassification.progression),
    names.slash_man_defeated: MM7ItemData(None, ItemClassification.progression),
    names.spring_man_defeated: MM7ItemData(None, ItemClassification.progression),
    names.shade_man_defeated: MM7ItemData(None, ItemClassification.progression),
    names.turbo_man_defeated: MM7ItemData(None, ItemClassification.progression),

    names.guts_man_g_defeated: MM7ItemData(None, ItemClassification.progression),
    names.gamerizer_defeated: MM7ItemData(None, ItemClassification.progression),
    names.hannya_ned_defeated: MM7ItemData(None, ItemClassification.progression),

    # Goal — locked event item
    names.wily_capsule: MM7ItemData(None, ItemClassification.progression),

    # ========================================================
    # Filler
    # ========================================================
    names.one_up: MM7ItemData(0x26, ItemClassification.filler, 2),
    names.e_tank: MM7ItemData(0x29, ItemClassification.filler, 2),
    names.w_tank: MM7ItemData(0x2A, ItemClassification.filler, 2),
    names.s_tank: MM7ItemData(0x2B, ItemClassification.filler, 1),
}


# ============================================================
# Derived tables
# ============================================================

item_name_to_id: Dict[str, int] = {
    item_name: MM7_ITEM_ID_BASE + data.code
    for item_name, data in item_table.items()
    if data.code is not None
}

item_id_to_name: Dict[int, str] = {
    item_id: item_name
    for item_name, item_id in item_name_to_id.items()
}

progression_items: Set[str] = {
    item_name
    for item_name, data in item_table.items()
    if data.classification & ItemClassification.progression
}

useful_items: Set[str] = {
    item_name
    for item_name, data in item_table.items()
    if data.classification == ItemClassification.useful
}

filler_items: List[str] = [
    item_name
    for item_name, data in item_table.items()
    if data.classification == ItemClassification.filler
]

event_items: Set[str] = {
    item_name
    for item_name, data in item_table.items()
    if data.code is None
}

weapon_items: Set[str] = {
    names.freeze_cracker,
    names.danger_wrap,
    names.thunder_bolt,
    names.junk_shield,
    names.slash_claw,
    names.wild_coil,
    names.noise_crush,
    names.scorch_wheel,
}

rush_items: Set[str] = {
    names.rush_coil,
    names.rush_search,
    names.rush_jet,
}

rush_plate_items: Set[str] = {
    names.rush_r_plate,
    names.rush_u_plate,
    names.rush_s_plate,
    names.rush_h_plate,
}

access_code_items: Set[str] = {
    names.wily_1_access,
    names.wily_2_access,
    names.wily_3_access,
}

item_groups: Dict[str, Set[str]] = {
    "Weapons": weapon_items,
    "Rush Items": rush_items,
    "Rush Plates": rush_plate_items,
    "Access Codes": access_code_items,
    "Filler": set(filler_items),
}

rom_receive_id = {
    names.freeze_cracker: 0x01,
    names.danger_wrap: 0x02,
    names.thunder_bolt: 0x03,
    names.junk_shield: 0x04,
    names.slash_claw: 0x05,
    names.wild_coil: 0x06,
    names.noise_crush: 0x07,
    names.scorch_wheel: 0x08,
    names.rush_coil: 0x09,
    names.rush_search: 0x0A,
    names.rush_jet: 0x0B,

    names.rush_r_plate: 0x0C,
    names.rush_u_plate: 0x0D,
    names.rush_s_plate: 0x0E,
    names.rush_h_plate: 0x0F,

    names.hyper_bolt: 0x10,
    names.exit_unit: 0x11,
    names.hyper_rocket_buster: 0x12,
    names.energy_balancer: 0x13,

    names.proto_shield: 0x14,
    names.beat: 0x15,

    names.one_up: 0x16,
    names.e_tank: 0x19,
    names.w_tank: 0x1A,
    names.s_tank: 0x1B,

    names.proto_man_cloud_man: 0x1D,
    names.proto_man_turbo_man: 0x1E,
    names.wily_1_access: 0x1F,
    names.wily_2_access: 0x20,
    names.wily_3_access: 0x21,
}


# ============================================================
# Creation helpers
# ============================================================

def create_item(name: str, player: int) -> MM7Item:
    data = item_table[name]
    code = None if data.code is None else MM7_ITEM_ID_BASE + data.code
    return MM7Item(name, data.classification, code, player)


def create_event(name: str, player: int) -> MM7Item:
    return MM7Item(name, ItemClassification.progression, None, player)


def get_filler_item_name(world) -> str:
    """Return one weighted filler item name.

    This expects an Archipelago World instance so it can use the world's RNG.
    """
    weighted_filler: List[str] = []
    for item_name in filler_items:
        weighted_filler.extend([item_name] * item_table[item_name].count)
    return world.random.choice(weighted_filler)


def get_pool_items() -> List[str]:
    """Return all non-event item names, expanding item counts.

    This is useful for building the base item pool before trimming or padding
    against the final number of randomized locations.
    """
    pool: List[str] = []
    for item_name, data in item_table.items():
        if data.code is None:
            continue
        pool.extend([item_name] * data.count)
    return pool
