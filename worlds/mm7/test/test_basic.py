from .bases import MM7TestBase


class TestDefaultLogic(MM7TestBase):
    options = {
        "logic_boss_weakness": True,
    }


class TestNoBossWeaknessLogic(MM7TestBase):
    options = {
        "logic_boss_weakness": False,
    }