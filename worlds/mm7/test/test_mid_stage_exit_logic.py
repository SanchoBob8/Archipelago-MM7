from .. import names
from .bases import MM7TestBase


class TestMidStageExitByBossDefeat(MM7TestBase):
    options = {
        "logic_boss_weakness": True,
        "exit_unit_in_uncleared_stages": False,
        "paid_exit_unit": False,
        "paid_exit_unit_in_logic": False,
    }

    def test_cloud_man_mega_bolt_can_exit_by_defeating_boss(self):
        self.assertAccessDependency(
            [names.mega_bolt_cloud_man_loc],
            [[names.rush_search, names.danger_wrap]],
            only_check_listed=True,
        )
class TestMidStageExitWithRealExitUnitClearedStage(MM7TestBase):
    options = {
        "logic_boss_weakness": True,
        "exit_unit_in_uncleared_stages": False,
        "paid_exit_unit": False,
        "paid_exit_unit_in_logic": False,
    }

    def test_cloud_man_mega_bolt_can_exit_with_exit_unit_after_stage_clear(self):
        self.assertAccessDependency(
            [names.mega_bolt_cloud_man_loc],
            [[names.rush_search, names.exit_unit, names.cloud_man_defeated]],
            only_check_listed=True,
        )


class TestMidStageExitWithRealExitUnitUnclearedStages(MM7TestBase):
    options = {
        "logic_boss_weakness": True,
        "exit_unit_in_uncleared_stages": True,
        "paid_exit_unit": False,
        "paid_exit_unit_in_logic": False,
    }

    def test_cloud_man_mega_bolt_can_exit_with_exit_unit_in_uncleared_stage(self):
        self.assertAccessDependency(
            [names.mega_bolt_cloud_man_loc],
            [[names.rush_search, names.exit_unit]],
            only_check_listed=True,
        )


class TestPaidExitUnitInLogic(MM7TestBase):
    options = {
        "logic_boss_weakness": True,
        "exit_unit_in_uncleared_stages": True,
        "paid_exit_unit": True,
        "paid_exit_unit_in_logic": True,
    }

    def test_paid_exit_unit_can_satisfy_mid_stage_exit_logic(self):
        self.assertAccessDependency(
            [names.mega_bolt_cloud_man_loc],
            [[names.rush_search]],
            only_check_listed=True,
        )