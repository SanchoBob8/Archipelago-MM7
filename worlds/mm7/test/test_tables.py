import unittest
from collections import Counter

from .. import names
from ..items import (
    get_pool_items,
    item_table,
    robot_master_access_codes,
    rom_receive_id,
)
from ..locations import (
    active_locations,
    event_location_to_item,
    event_locations,
    location_name_to_id,
    location_table,
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
    def test_pool_matches_randomized_locations_for_every_starter(
        self,
    ) -> None:
        randomized_active_locations = [
            location_name
            for location_name in active_locations
            if location_name not in event_locations
        ]

        for starter_access_code in robot_master_access_codes:
            with self.subTest(starter=starter_access_code):
                pool = get_pool_items(
                    excluded_items={starter_access_code}
                )

                self.assertEqual(
                    len(randomized_active_locations),
                    len(pool),
                )

                self.assertNotIn(
                    starter_access_code,
                    pool,
                )

                for access_code in robot_master_access_codes:
                    if access_code != starter_access_code:
                        self.assertIn(access_code, pool)
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

    def test_rom_receive_items_exist_in_item_table(self) -> None:
        for item_name in rom_receive_id:
            with self.subTest(item=item_name):
                self.assertIn(
                    item_name,
                    item_table,
                    f"{item_name} has a ROM receive ID but is missing from item_table.",
                )

    def test_rom_receive_ids_are_unique(self) -> None:
        receive_ids = list(rom_receive_id.values())

        self.assertEqual(
            len(receive_ids),
            len(set(receive_ids)),
            "Every MM7 item must have a unique ROM receive ID.",
        )

    def test_robot_master_access_items_exist(self) -> None:
        for item_name in robot_master_access_codes:
            with self.subTest(item=item_name):
                self.assertIn(item_name, item_table)


    def test_robot_master_access_items_have_rom_receive_ids(
        self,
    ) -> None:
        expected = {
            names.freeze_man_access: 0x22,
            names.cloud_man_access: 0x23,
            names.junk_man_access: 0x24,
            names.turbo_man_access: 0x25,
            names.slash_man_access: 0x26,
            names.shade_man_access: 0x27,
            names.burst_man_access: 0x28,
            names.spring_man_access: 0x29,
        }

        for item_name, receive_id in expected.items():
            with self.subTest(item=item_name):
                self.assertEqual(
                    receive_id,
                    rom_receive_id[item_name],
                )
