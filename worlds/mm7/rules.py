# worlds/mm7/rules.py

from typing import TYPE_CHECKING

from BaseClasses import CollectionState, MultiWorld
from worlds.AutoWorld import World

from . import names

if TYPE_CHECKING:
    from . import MegaMan7World

MAIN_BOSSES = [
    names.burst_man_defeated,
    names.cloud_man_defeated,
    names.junk_man_defeated,
    names.freeze_man_defeated,
    names.slash_man_defeated,
    names.spring_man_defeated,
    names.shade_man_defeated,
    names.turbo_man_defeated,
]


BOSS_ITEM_LOCATION_TABLE = {
    names.burst_man_defeated: names.burst_man_defeated_item,
    names.cloud_man_defeated: names.cloud_man_defeated_item,
    names.junk_man_defeated: names.junk_man_defeated_item,
    names.freeze_man_defeated: names.freeze_man_defeated_item,
    names.slash_man_defeated: names.slash_man_defeated_item,
    names.spring_man_defeated: names.spring_man_defeated_item,
    names.shade_man_defeated: names.shade_man_defeated_item,
    names.turbo_man_defeated: names.turbo_man_defeated_item,
}


WEAKNESS_TABLE = {
    names.burst_man_defeated: [names.freeze_cracker, names.scorch_wheel],
    names.cloud_man_defeated: [names.danger_wrap],
    names.junk_man_defeated: [names.thunder_bolt],
    names.freeze_man_defeated: [names.junk_shield, names.scorch_wheel],
    names.slash_man_defeated: [names.freeze_cracker, names.scorch_wheel],
    names.spring_man_defeated: [names.slash_claw],
    names.shade_man_defeated: [names.wild_coil],
    names.turbo_man_defeated: [names.noise_crush],
    names.mash_defeated: [names.danger_wrap],
    names.guts_man_g_defeated: [names.slash_claw],
    names.gamerizer_defeated: [names.wild_coil, names.danger_wrap],
    names.hannya_ned_defeated: [names.slash_claw, names.noise_crush],
    names.wily_capsule: [names.wild_coil]
}


def always_accessible(state: CollectionState) -> bool:
    return True


def has_any(state: CollectionState, player: int, items: list[str]) -> bool:
    return any(state.has(item, player) for item in items)


def has_all(state: CollectionState, player: int, items: list[str]) -> bool:
    return all(state.has(item, player) for item in items)


def defeated_boss_count(state: CollectionState, player: int) -> int:
    return sum(state.has(boss, player) for boss in MAIN_BOSSES)


def has_robot_museum_access(state: CollectionState, player: int) -> bool:
    return defeated_boss_count(state, player) >= 4


def has_wily_1_access(state: CollectionState, player: int) -> bool:
    return state.has(names.wily_1_access, player)


def has_wily_2_access(state: CollectionState, player: int) -> bool:
    return state.has(names.wily_2_access, player)


def has_wily_3_access(state: CollectionState, player: int) -> bool:
    return state.has(names.wily_3_access, player)


def has_wily_4_access(state: CollectionState, world: "MegaMan7World") -> bool:
    player = world.player
    requirement_type = world.options.wily_4_requirement_type.value

    if requirement_type == world.options.wily_4_requirement_type.option_wily_stages:
        required = world.options.wily_4_wily_stages.value

        cleared_wily_stages = sum(
            [
                state.has(names.guts_man_g_defeated, player),
                state.has(names.gamerizer_defeated, player),
                state.has(names.hannya_ned_defeated, player),
            ]
        )

        return cleared_wily_stages >= required

    if requirement_type == world.options.wily_4_requirement_type.option_robot_masters:
        required = world.options.wily_4_robot_masters.value

        defeated_robot_masters = sum(
            [
                state.has(names.freeze_man_defeated, player),
                state.has(names.cloud_man_defeated, player),
                state.has(names.junk_man_defeated, player),
                state.has(names.burst_man_defeated, player),
                state.has(names.slash_man_defeated, player),
                state.has(names.spring_man_defeated, player),
                state.has(names.shade_man_defeated, player),
                state.has(names.turbo_man_defeated, player),
            ]
        )

        return defeated_robot_masters >= required

    if requirement_type == world.options.wily_4_requirement_type.option_weapons:
        required = world.options.wily_4_weapons.value

        weapons_received = sum(
            [
                state.has(names.freeze_cracker, player),
                state.has(names.danger_wrap, player),
                state.has(names.thunder_bolt, player),
                state.has(names.junk_shield, player),
                state.has(names.slash_claw, player),
                state.has(names.wild_coil, player),
                state.has(names.noise_crush, player),
                state.has(names.scorch_wheel, player),
            ]
        )

        return weapons_received >= required

    return False


# Super Adapter is not an AP item.
# In logic, it is derived from all four Rush plates.
def has_super_adapter(state: CollectionState, player: int) -> bool:
    return has_all(
        state,
        player,
        [
            names.rush_r_plate,
            names.rush_u_plate,
            names.rush_s_plate,
            names.rush_h_plate,
        ],
    )


def can_traverse_vertical(state: CollectionState, player: int) -> bool:
    return state.has(names.rush_coil, player) or state.has(names.rush_jet, player) or has_super_adapter(state, player)


def can_use_rush_search_and_exit(
    state: CollectionState,
    player: int,
    world: "MegaMan7World",
    stage_clear_event: str,
) -> bool:
    return state.has(names.rush_search, player) and can_leave_stage_after_check(state, world, stage_clear_event)


def can_buy_shop_upgrade(state: CollectionState, player: int) -> bool:
    # Current ROM/shop model:
    # shop is accessible by default, but special shop upgrades require Hyper Bolt.
    return state.has(names.hyper_bolt, player)


def can_get_rush_search_and_exit_or_buy_shop_upgrade(
    state: CollectionState, player: int, world: "MegaMan7World", stage_clear_event: str
) -> bool:
    return can_use_rush_search_and_exit(state, player, world, stage_clear_event) or can_buy_shop_upgrade(state, player)


def can_defeat_boss(state: CollectionState, player: int, boss: str) -> bool:
    if boss not in WEAKNESS_TABLE:
        return True

    return has_any(state, player, WEAKNESS_TABLE[boss])


def can_use_exit_unit_after_check(
    state: CollectionState,
    world: "MegaMan7World",
    stage_clear_event: str,
) -> bool:
    player = world.player

    can_exit_this_stage = world.options.exit_unit_in_uncleared_stages.value or state.has(stage_clear_event, player)

    if not can_exit_this_stage:
        return False

    if state.has(names.exit_unit, player):
        return True

    return world.options.paid_exit_unit.value and world.options.paid_exit_unit_in_logic.value


def can_leave_stage_after_check(
    state: CollectionState,
    world: "MegaMan7World",
    stage_clear_event: str,
) -> bool:
    player = world.player

    if not world.options.logic_boss_weakness.value:
        return True

    return can_defeat_boss(state, player, stage_clear_event) or can_use_exit_unit_after_check(
        state, world, stage_clear_event
    )


def set_rules(world: World, multiworld: MultiWorld, player: int) -> None:
    # ============================================================
    # Main boss locations
    #
    # Current MVP ROM:
    # - All 8 Robot Master stages are open from the start.
    # - If logic_boss_weakness is disabled, bosses are open.
    # - If enabled, boss medal and boss item location require a weakness.
    # ============================================================

    for boss, item_location in BOSS_ITEM_LOCATION_TABLE.items():
        if world.options.logic_boss_weakness.value:
            multiworld.get_location(boss, player).access_rule = lambda state, b=boss: can_defeat_boss(state, player, b)

            multiworld.get_location(item_location, player).access_rule = lambda state, b=boss: can_defeat_boss(
                state, player, b
            )
        else:
            multiworld.get_location(boss, player).access_rule = always_accessible
            multiworld.get_location(item_location, player).access_rule = always_accessible

    # ============================================================
    # Intro Stage / Rush Coil
    #
    # Current ROM starts from Intro Stage and checks Rush Coil on clear.
    # ============================================================

    multiworld.get_location(names.rush_coil_loc, player).access_rule = always_accessible

    # ============================================================
    # Robot Museum / Mash
    #
    # ROM routing is based on AP boss medals.
    # ============================================================

    multiworld.get_location(names.mash_defeated, player).access_rule = lambda state: has_robot_museum_access(
        state, player
    )

    # ============================================================
    # Proto Man
    #
    # Cloud/Turbo meetings are currently reachable through open stages.
    # Proto Shield requires both AP Proto clue items.
    # ============================================================

    multiworld.get_location(names.proto_man_cloud_man_loc, player).access_rule = lambda state: (
        can_traverse_vertical(state, player) and can_leave_stage_after_check(state, world, names.cloud_man_defeated)
    )

    multiworld.get_location(names.proto_man_turbo_man_loc, player).access_rule = lambda state: (
        can_leave_stage_after_check(state, world, names.turbo_man_defeated)
    )

    multiworld.get_location(names.proto_shield_loc, player).access_rule = lambda state: (
        state.has(names.proto_man_cloud_man, player)
        and state.has(names.proto_man_turbo_man, player)
        and can_leave_stage_after_check(state, world, names.shade_man_defeated)
    )

    # ============================================================
    # Rush plates and unique items
    # ============================================================

    multiworld.get_location(names.rush_r_plate_loc, player).access_rule = lambda state: can_leave_stage_after_check(
        state, world, names.burst_man_defeated
    )

    multiworld.get_location(names.rush_u_plate_loc, player).access_rule = lambda state: (
        can_traverse_vertical(state, player) and can_leave_stage_after_check(state, world, names.cloud_man_defeated)
    )

    multiworld.get_location(names.rush_s_plate_loc, player).access_rule = lambda state: (
        state.has(names.freeze_cracker, player) and can_leave_stage_after_check(state, world, names.junk_man_defeated)
    )

    multiworld.get_location(names.rush_h_plate_loc, player).access_rule = lambda state: (
        can_traverse_vertical(state, player) and can_leave_stage_after_check(state, world, names.freeze_man_defeated)
    )

    multiworld.get_location(names.hyper_bolt_loc, player).access_rule = lambda state: can_leave_stage_after_check(
        state, world, names.spring_man_defeated
    )

    # Exit Unit can be checked either by Rush Search in-stage or by buying it in the shop (no hyper bolt needed).
    # To prevent the logic expecting the player to farm 200 bolts right at the start, for now
    # we only take the in-stage location.
    multiworld.get_location(names.exit_unit_loc, player).access_rule = lambda state: can_use_rush_search_and_exit(
        state, player, world, names.freeze_man_defeated
    )

    # Hyper Rocket Buster can be checked either:
    # - by Rush Search in-stage
    # - or by buying it in the shop with Hyper Bolt
    #
    # ROM shop Super Adapter requirement has been removed.
    multiworld.get_location(names.hyper_rocket_buster_loc, player).access_rule = lambda state: (
        can_get_rush_search_and_exit_or_buy_shop_upgrade(state, player, world, names.turbo_man_defeated)
    )

    # Energy Balancer can be checked either:
    # - by Rush Search in-stage
    # - or by buying it in the shop with Hyper Bolt
    multiworld.get_location(names.energy_balancer_loc, player).access_rule = lambda state: (
        can_get_rush_search_and_exit_or_buy_shop_upgrade(state, player, world, names.shade_man_defeated)
    )

    # Beat is in Slash Man stage.
    # Keep actual item requirements, but no slash_man_access gate.
    multiworld.get_location(names.beat_loc, player).access_rule = lambda state: (
        state.has(names.scorch_wheel, player)
        and can_traverse_vertical(state, player)
        and can_leave_stage_after_check(state, world, names.slash_man_defeated)
    )

    # ============================================================
    # Rush items
    # ============================================================

    # Rush Search can be checked in-stage or be bought after getting the hyper bolt.
    multiworld.get_location(names.rush_search_loc, player).access_rule = lambda state: (
        can_leave_stage_after_check(state, world, names.freeze_man_defeated) or can_buy_shop_upgrade(state, player)
    )

    # Rush Jet can be checked either in-stage with Thunder Bolt or be bought after getting the hyper bolt.
    multiworld.get_location(names.rush_jet_loc, player).access_rule = lambda state: (
        can_buy_shop_upgrade(state, player)
        or (
            state.has(names.thunder_bolt, player) and can_leave_stage_after_check(state, world, names.junk_man_defeated)
        )
    )

    # ============================================================
    # Mega Bolts and Mega Health Capsule
    #
    # All are Rush Search checks.
    # Keep extra item requirements only where the pickup route actually
    # requires them.
    # ============================================================

    multiworld.get_location(names.mega_bolt_cloud_man_loc, player).access_rule = lambda state: (
        can_use_rush_search_and_exit(state, player, world, names.cloud_man_defeated)
    )

    multiworld.get_location(names.mega_bolt_spring_man_loc, player).access_rule = lambda state: (
        can_use_rush_search_and_exit(state, player, world, names.spring_man_defeated)
    )

    multiworld.get_location(names.mega_bolt_shade_man_loc, player).access_rule = lambda state: (
        can_use_rush_search_and_exit(state, player, world, names.shade_man_defeated)
    )

    multiworld.get_location(names.mega_bolt_turbo_man_loc, player).access_rule = lambda state: (
        can_use_rush_search_and_exit(state, player, world, names.turbo_man_defeated)
    )

    multiworld.get_location(names.mega_bolt_junk_man_loc, player).access_rule = lambda state: (
        state.has(names.freeze_cracker, player)
        and can_use_rush_search_and_exit(state, player, world, names.junk_man_defeated)
    )

    multiworld.get_location(names.mega_health_capsule_loc, player).access_rule = lambda state: (
        can_use_rush_search_and_exit(state, player, world, names.spring_man_defeated)
    )

    # ============================================================
    # Wily stages
    #
    # Base design:
    # - Wily 1/2/3 are unlocked independently by access-code items.
    # - They can be cleared in any order.
    # - Wily 4 / Wily Capsule unlocks after Wily 1/2/3 are cleared.
    # ============================================================

    multiworld.get_location(names.guts_man_g_defeated, player).access_rule = lambda state: (
        has_wily_1_access(state, player) and can_traverse_vertical(state, player)
    )

    multiworld.get_location(names.guts_man_g_defeated_item, player).access_rule = lambda state: (
        has_wily_1_access(state, player) and can_traverse_vertical(state, player)
    )

    multiworld.get_location(names.gamerizer_defeated, player).access_rule = lambda state: (
        has_wily_2_access(state, player)
        and (can_traverse_vertical(state, player) or state.has(names.freeze_cracker, player))
    )

    multiworld.get_location(names.gamerizer_defeated_item, player).access_rule = lambda state: (
        has_wily_2_access(state, player)
        and (can_traverse_vertical(state, player) or state.has(names.freeze_cracker, player))
    )

    multiworld.get_location(names.hannya_ned_defeated, player).access_rule = lambda state: (
        has_wily_3_access(state, player) and can_traverse_vertical(state, player)
    )

    multiworld.get_location(names.hannya_ned_defeated_item, player).access_rule = lambda state: (
        has_wily_3_access(state, player) and can_traverse_vertical(state, player)
    )

    multiworld.get_location(names.wily_capsule, player).access_rule = lambda state: has_wily_4_access(state, world)

    multiworld.completion_condition[player] = lambda state: state.has(names.wily_capsule, player)
