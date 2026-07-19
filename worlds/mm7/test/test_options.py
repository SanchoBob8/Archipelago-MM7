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

class TestPaidExitUnitDisabled(MM7TestBase):
    options = {
        "paid_exit_unit": False,
        "paid_exit_unit_cost": 100,
        "exit_unit_in_uncleared_stages": False,
    }


class TestPaidExitUnitEnabled(MM7TestBase):
    options = {
        "paid_exit_unit": True,
        "paid_exit_unit_cost": 100,
        "exit_unit_in_uncleared_stages": False,
    }


class TestPaidExitUnitMinimumCost(MM7TestBase):
    options = {
        "paid_exit_unit": True,
        "paid_exit_unit_cost": 0,
        "exit_unit_in_uncleared_stages": False,
    }


class TestPaidExitUnitMaximumCost(MM7TestBase):
    options = {
        "paid_exit_unit": True,
        "paid_exit_unit_cost": 999,
        "exit_unit_in_uncleared_stages": False,
    }


class TestExitUnitInUnclearedStages(MM7TestBase):
    options = {
        "paid_exit_unit": False,
        "paid_exit_unit_cost": 100,
        "exit_unit_in_uncleared_stages": True,
    }


class TestPaidExitUnitInUnclearedStages(MM7TestBase):
    options = {
        "paid_exit_unit": True,
        "paid_exit_unit_cost": 100,
        "exit_unit_in_uncleared_stages": True,
    }

class TestAllResourceAndExitUnitOptionsMaximums(MM7TestBase):
    options = {
        "starting_lives": 9,
        "starting_bolts": 999,
        "starting_e_tanks": 4,
        "starting_w_tanks": 4,
        "starting_s_tanks": 1,
        "paid_exit_unit": True,
        "paid_exit_unit_cost": 999,
        "exit_unit_in_uncleared_stages": True,
    }