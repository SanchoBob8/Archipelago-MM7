from .. import names
from ..locations import (
    MM7_LOCATION_ID_BASE,
    location_name_to_id,
    pickupsanity_locations,
)
from .bases import MM7TestBase


class TestPickupsanityEnabled(MM7TestBase):
    options = {
        "pickupsanity": True,
        "logic_boss_weakness": False,
    }

    def test_pickupsanity_locations_are_created_and_mapped(self) -> None:
        created_locations = {
            location.name
            for location in self.multiworld.get_locations(self.player)
        }

        self.assertEqual(72, len(pickupsanity_locations))
        self.assertEqual(72, len(set(pickupsanity_locations)))

        self.assertTrue(
            set(pickupsanity_locations).issubset(created_locations)
        )

        self.assertEqual(
            [
                MM7_LOCATION_ID_BASE + code
                for code in range(0x40, 0x88)
            ],
            [
                location_name_to_id[location_name]
                for location_name in pickupsanity_locations
            ],
        )

        self.assertTrue(
            self.world.fill_slot_data()["pickupsanity"]
        )


class TestPickupsanityExitUnitUnclearedDisabled(MM7TestBase):
    options = {
        "pickupsanity": True,
        "logic_boss_weakness": True,
        "robot_master_access_codes": False,
        "exit_unit_in_uncleared_stages": False,
        "paid_exit_unit": False,
    }

    def test_exit_unit_does_not_unlock_uncleared_pickup(self) -> None:
        state = self.multiworld.state
        location = self.multiworld.get_location(
            names.spring_man_large_bolt,
            self.player,
        )

        state.collect(
            self.world.create_item(names.exit_unit),
            True,
        )

        self.assertFalse(location.can_reach(state))


class TestPickupsanityExitUnitUnclearedEnabled(MM7TestBase):
    options = {
        "pickupsanity": True,
        "logic_boss_weakness": True,
        "robot_master_access_codes": False,
        "exit_unit_in_uncleared_stages": True,
        "paid_exit_unit": False,
    }

    def test_exit_unit_unlocks_uncleared_pickup(self) -> None:
        state = self.multiworld.state
        location = self.multiworld.get_location(
            names.spring_man_large_bolt,
            self.player,
        )

        state.collect(
            self.world.create_item(names.exit_unit),
            True,
        )

        self.assertTrue(location.can_reach(state))