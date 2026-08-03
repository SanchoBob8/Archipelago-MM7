from BaseClasses import CollectionState

from .. import names
from .bases import MM7TestBase


ROBOT_MASTER_EVENTS = [
    names.burst_man_defeated,
    names.cloud_man_defeated,
    names.junk_man_defeated,
    names.freeze_man_defeated,
    names.slash_man_defeated,
    names.spring_man_defeated,
    names.shade_man_defeated,
    names.turbo_man_defeated,
]


class TestRobotMuseumLogic(MM7TestBase):
    options = {
        "logic_boss_weakness": True,
        "skip_robot_museum": True,
        "robot_museum_robot_masters": 4,
    }

    def collect_robot_masters(
        self,
        state: CollectionState,
        count: int,
    ) -> None:
        for boss_event in ROBOT_MASTER_EVENTS[:count]:
            state.collect(self.get_item_by_name(boss_event))

    def test_robot_museum_requirements_1_4_and_8(self) -> None:
        mash = self.multiworld.get_location(
            names.mash_defeated,
            self.player,
        )

        # Museum skipping bypasses the Mash weakness, allowing this test
        # to isolate only the configurable Robot Master requirement.
        self.world.options.skip_robot_museum.value = 1

        for required in (1, 4, 8):
            with self.subTest(required=required):
                self.world.options.robot_museum_robot_masters.value = required

                state = CollectionState(self.multiworld)

                self.collect_robot_masters(state, required - 1)

                self.assertFalse(
                    mash.can_reach(state),
                    f"Mash should not be reachable with only "
                    f"{required - 1} Robot Masters when {required} are required.",
                )

                state.collect(
                    self.get_item_by_name(
                        ROBOT_MASTER_EVENTS[required - 1]
                    )
                )

                self.assertTrue(
                    mash.can_reach(state),
                    f"Mash should be reachable after defeating "
                    f"{required} Robot Masters.",
                )

    def test_non_skipped_museum_requires_mash_weakness(self) -> None:
        self.world.options.skip_robot_museum.value = 0
        self.world.options.robot_museum_robot_masters.value = 4

        state = CollectionState(self.multiworld)
        self.collect_robot_masters(state, 4)

        mash = self.multiworld.get_location(
            names.mash_defeated,
            self.player,
        )

        self.assertFalse(
            mash.can_reach(state),
            "Mash should require Danger Wrap when Robot Museum is not skipped.",
        )

        state.collect(self.get_item_by_name(names.danger_wrap))

        self.assertTrue(
            mash.can_reach(state),
            "Mash should be reachable with four Robot Masters and Danger Wrap.",
        )

    def test_skipped_museum_does_not_require_mash_weakness(self) -> None:
        self.world.options.skip_robot_museum.value = 1
        self.world.options.robot_museum_robot_masters.value = 4

        state = CollectionState(self.multiworld)
        self.collect_robot_masters(state, 3)

        mash = self.multiworld.get_location(
            names.mash_defeated,
            self.player,
        )

        self.assertFalse(
            mash.can_reach(state),
            "Skipping Robot Museum must not bypass the Robot Master requirement.",
        )

        state.collect(
            self.get_item_by_name(ROBOT_MASTER_EVENTS[3])
        )

        self.assertTrue(
            mash.can_reach(state),
            "Skipped Robot Museum should award Mash at the configured threshold "
            "without requiring Danger Wrap.",
        )