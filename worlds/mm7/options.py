from dataclasses import dataclass

from Options import Range, Toggle, PerGameCommonOptions


class LogicBossWeakness(Toggle):
    """
    Every main boss will logically expect you to have its weakness.
    """
    display_name = "Boss Weakness Logic"
    default = True


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
    default = 1


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


@dataclass
class MegaMan7Options(PerGameCommonOptions):
    logic_boss_weakness: LogicBossWeakness
    starting_lives: StartingLives
    starting_bolts: StartingBolts
    starting_e_tanks: StartingETanks
    starting_w_tanks: StartingWTanks
    starting_s_tanks: StartingSTanks