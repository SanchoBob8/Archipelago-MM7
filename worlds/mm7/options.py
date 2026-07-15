from dataclasses import dataclass
from Options import Toggle, PerGameCommonOptions

class LogicBossWeakness(Toggle):
    """
    Every main boss will logically expect you to have its weakness.
    """
    display_name = "Boss Weakness Logic"
    default = True


@dataclass
class MegaMan7Options(PerGameCommonOptions):
    logic_boss_weakness: LogicBossWeakness