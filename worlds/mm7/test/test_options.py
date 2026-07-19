from .bases import MM7TestBase


class TestStartingResourceDefaults(MM7TestBase):
    options = {
        "logic_boss_weakness": True,
    }


class TestStartingResourceMinimums(MM7TestBase):
    options = {
        "starting_lives": 1,
        "starting_bolts": 0,
        "starting_e_tanks": 0,
        "starting_w_tanks": 0,
        "starting_s_tanks": 0,
    }


class TestStartingResourceMaximums(MM7TestBase):
    options = {
        "starting_lives": 9,
        "starting_bolts": 999,
        "starting_e_tanks": 4,
        "starting_w_tanks": 4,
        "starting_s_tanks": 1,
    }