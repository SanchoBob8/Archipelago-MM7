from dataclasses import dataclass

from Options import Choice, DeathLink, OptionGroup, PerGameCommonOptions, Range, Toggle


class LogicBossWeakness(Toggle):
    """
    Every main boss will logically expect you to have its weakness.
    """
    display_name = "Boss Weakness Logic"
    default = False

class RobotMasterAccessCodes(Toggle):
    """
    Locks each Robot Master stage behind its corresponding Access Code.

    One random Robot Master Access Code is granted at the start so that
    at least one stage is immediately available.
    """

    display_name = "Robot Master Access Codes"
    default = False

class StartingLives(Range):
    """
    Number of lives Mega Man starts with.
    """
    display_name = "Starting Lives"
    range_start = 1
    range_end = 9
    default = 3


class StartingBolts(Range):
    """
    Number of bolts Mega Man starts with.
    """
    display_name = "Starting Bolts"
    range_start = 0
    range_end = 999
    default = 0


class StartingETanks(Range):
    """
    Number of E-Tanks Mega Man starts with.
    """
    display_name = "Starting E-Tanks"
    range_start = 0
    range_end = 4
    default = 0


class StartingWTanks(Range):
    """
    Number of W-Tanks Mega Man starts with.
    """
    display_name = "Starting W-Tanks"
    range_start = 0
    range_end = 4
    default = 0


class StartingSTanks(Range):
    """
    Number of S-Tanks Mega Man starts with.
    """
    display_name = "Starting S-Tanks"
    range_start = 0
    range_end = 1
    default = 0

class ExitUnitInUnclearedStages(Toggle):
    """
    Allows the Exit Unit to be used before the current stage has been cleared.
    """
    display_name = "Exit Unit in Uncleared Stages"
    default = False

class PaidExitUnit(Toggle):
    """
    Allows the Exit Unit to be used before receiving the Exit Unit item by spending bolts.
    """
    display_name = "Paid Exit Unit"
    default = False


class PaidExitUnitCost(Range):
    """
    Number of bolts required to use the Exit Unit before receiving the Exit Unit item.
    """
    display_name = "Paid Exit Unit Cost"
    range_start = 0
    range_end = 999
    default = 100

class PaidExitUnitInLogic(Toggle):
    """
    Allows logic to consider Paid Exit Unit as a valid way to leave stages.
    This can make seeds expect the player to have enough bolts for paid exits.
    """
    display_name = "Paid Exit Unit in Logic"
    default = False

class Wily4RequirementType(Choice):
    """
    Determines what is required before Wily 4 becomes available.
    """
    display_name = "Wily 4 Requirement Type"

    option_wily_stages = 0
    option_robot_masters = 1
    option_weapons = 2

    default = option_wily_stages


class Wily4WilyStages(Range):
    """
    With Wily Stages requirement: set the number of Wily stages required to access Wily 4.
    """
    display_name = "Wily Stages Required for Wily 4"
    range_start = 0
    range_end = 3
    default = 3


class Wily4RobotMasters(Range):
    """
    With Robot Masters requirement: set the number of defeated Robot Masters required to access Wily 4.
    """
    display_name = "Robot Masters Required for Wily 4"
    range_start = 0
    range_end = 8
    default = 8


class Wily4Weapons(Range):
    """
    With Weapons requirement: set the number of Robot Master weapons required to access Wily 4.
    """
    display_name = "Weapons Required for Wily 4"
    range_start = 0
    range_end = 8
    default = 8

class SkipIntroStage(Toggle):
    """
    Starts the game after the Intro Stage and automatically get the corresponding check.
    """
    display_name = "Skip Intro Stage"
    default = False

class SkipRobotMuseum(Toggle):
    """
    Skips the Robot Museum stage and automatically awards the corresponding check
    when Robot Museum would normally become available.
    """

    display_name = "Skip Robot Museum"
    default = False

class RobotMastersRequiredForRobotMuseum(Range):
    """
    Number of defeated Robot Masters required before Robot Museum
    becomes available.
    """

    display_name = "Robot Masters Required for Robot Museum"
    range_start = 1
    range_end = 8
    default = 4

class CheckpointSelection(Toggle):
    """
    Allows L/R on the stage-select screen to choose between the entrance,
    midpoint, and pre-boss checkpoints for cleared Robot Master stages.
    """
    display_name = "Checkpoint Selection"
    default = True


class CheckpointSelectionInUnclearedStages(Toggle):
    """
    Allows checkpoint selection before a Robot Master stage has been cleared.
    Only applies when Checkpoint Selection is enabled.
    """
    display_name = "Checkpoint Selection in Uncleared Stages"
    default = False

class Pickupsanity(Toggle):
    """
    Adds freestanding stage pickups as Archipelago locations.

    Each unique pickup can be checked only once. After it has been checked,
    later respawns behave as normal vanilla pickups.
    """

    display_name = "Pickupsanity"
    default = False

@dataclass
class MegaMan7Options(PerGameCommonOptions):
    robot_master_access_codes: RobotMasterAccessCodes
    pickupsanity: Pickupsanity
    logic_boss_weakness: LogicBossWeakness

    skip_intro_stage: SkipIntroStage
    skip_robot_museum: SkipRobotMuseum
    robot_museum_robot_masters: RobotMastersRequiredForRobotMuseum

    checkpoint_selection: CheckpointSelection
    checkpoint_selection_in_uncleared_stages: CheckpointSelectionInUnclearedStages

    exit_unit_in_uncleared_stages: ExitUnitInUnclearedStages
    paid_exit_unit: PaidExitUnit
    paid_exit_unit_cost: PaidExitUnitCost
    paid_exit_unit_in_logic: PaidExitUnitInLogic

    wily_4_requirement_type: Wily4RequirementType
    wily_4_wily_stages: Wily4WilyStages
    wily_4_robot_masters: Wily4RobotMasters
    wily_4_weapons: Wily4Weapons

    starting_lives: StartingLives
    starting_bolts: StartingBolts
    starting_e_tanks: StartingETanks
    starting_w_tanks: StartingWTanks
    starting_s_tanks: StartingSTanks

    death_link: DeathLink

mm7_option_groups = [
    OptionGroup(
        "Progression and Logic",
        [
            RobotMasterAccessCodes,
            Pickupsanity,
            LogicBossWeakness,
        ],
    ),
    OptionGroup(
        "Stage Options",
        [
            SkipIntroStage,
            SkipRobotMuseum,
            RobotMastersRequiredForRobotMuseum,
            CheckpointSelection,
            CheckpointSelectionInUnclearedStages,
        ],
    ),
    OptionGroup(
        "Exit Unit Options",
        [
            ExitUnitInUnclearedStages,
            PaidExitUnit,
            PaidExitUnitCost,
            PaidExitUnitInLogic,
        ],
        start_collapsed=True,
    ),
    OptionGroup(
        "Wily 4 Options",
        [
            Wily4RequirementType,
            Wily4WilyStages,
            Wily4RobotMasters,
            Wily4Weapons,
        ],
        start_collapsed=True,
    ),
    OptionGroup(
        "Starting Resources",
        [
            StartingLives,
            StartingBolts,
            StartingETanks,
            StartingWTanks,
            StartingSTanks,
        ],
        start_collapsed=True,
    ),
    OptionGroup(
        "Multiplayer Options",
        [
            DeathLink,
        ],
        start_collapsed=True,
    ),
]
