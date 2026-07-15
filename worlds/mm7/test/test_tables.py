import unittest

from .. import names
from .. import ITEM_POOL
from ..items import item_table, rom_receive_id
from ..locations import (
    active_locations,
    location_table,
    location_name_to_id,
    event_locations,
    event_location_to_item,
    wily_boss_event_locations,
    wily_boss_item_locations,
)


class TestMM7Tables(unittest.TestCase):
    def test_wily_access_items_exist(self) -> None:
        for item_name in [
            names.wily_1_access,
            names.wily_2_access,
            names.wily_3_access,
        ]:
            with self.subTest(item=item_name):
                self.assertIn(item_name, item_table)

    def test_wily_access_items_have_rom_receive_ids(self) -> None:
        expected = {
            names.wily_1_access: 0x1F,
            names.wily_2_access: 0x20,
            names.wily_3_access: 0x21,
        }

        for item_name, receive_id in expected.items():
            with self.subTest(item=item_name):
                self.assertIn(item_name, rom_receive_id)
                self.assertEqual(receive_id, rom_receive_id[item_name])

    def test_wily_defeated_locations_are_events(self) -> None:
        for location_name in [
            names.guts_man_g_defeated,
            names.gamerizer_defeated,
            names.hannya_ned_defeated,
        ]:
            with self.subTest(location=location_name):
                self.assertIn(location_name, wily_boss_event_locations)
                self.assertIn(location_name, event_location_to_item)

    def test_wily_reward_locations_are_randomized(self) -> None:
        for location_name in [
            names.guts_man_g_defeated_item,
            names.gamerizer_defeated_item,
            names.hannya_ned_defeated_item,
        ]:
            with self.subTest(location=location_name):
                self.assertIn(location_name, wily_boss_item_locations)
                self.assertIn(location_name, active_locations)
                self.assertNotIn(location_name, event_location_to_item)

class TestMM7PoolTables(unittest.TestCase):
    def test_minimal_pool_matches_randomized_active_locations(self) -> None:
        randomized_active_locations = [
            location_name
            for location_name in active_locations
            if location_name not in event_locations
        ]

        self.assertEqual(
            len(randomized_active_locations),
            len(ITEM_POOL),
            "ITEM_POOL must contain exactly one item per randomized active location.",
        )
    def test_active_locations_exist_in_location_table(self) -> None:
        for location_name in active_locations:
            with self.subTest(location=location_name):
                self.assertIn(location_name, location_table)

    def test_event_locations_have_no_ap_code(self) -> None:
        for location_name in event_location_to_item:
            with self.subTest(location=location_name):
                self.assertIsNone(location_table[location_name].code)

    def test_randomized_active_locations_have_location_ids(self) -> None:
        for location_name in active_locations:
            if location_name in event_locations:
                continue

            with self.subTest(location=location_name):
                self.assertIn(location_name, location_name_to_id)