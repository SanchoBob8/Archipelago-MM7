from ..rom import MM7_ROM_CONFIG_SIZE, get_rom_config
from .bases import MM7TestBase


class TestDefaultRomConfig(MM7TestBase):
    def test_default_rom_config(self) -> None:
        config = get_rom_config(self.world)

        self.assertEqual(MM7_ROM_CONFIG_SIZE, 17)
        self.assertEqual(len(config), MM7_ROM_CONFIG_SIZE)

        self.assertEqual(
            config,
            bytes([
                3,      # Starting lives
                0,      # Starting E-Tanks
                0,      # Starting W-Tanks
                0,      # Starting S-Tanks
                0x00,   # Starting bolts low
                0x00,   # Starting bolts high
                0,      # Paid Exit Unit
                0x64,   # Paid Exit Unit cost low: 100
                0x00,   # Paid Exit Unit cost high
                0,      # Exit Unit in uncleared stages
                0,      # Wily 4 requirement type: Wily stages
                3,      # Wily stages required
                8,      # Robot Masters required for Wily 4
                8,      # Weapons required for Wily 4
                0,      # Skip Intro Stage
                0,      # Skip Robot Museum
                4,      # Robot Masters required for Robot Museum
            ]),
        )


class TestCustomRomConfig(MM7TestBase):
    options = {
        "starting_lives": 7,
        "starting_bolts": 554,  # $022A
        "starting_e_tanks": 1,
        "starting_w_tanks": 2,
        "starting_s_tanks": 1,
        "paid_exit_unit": True,
        "paid_exit_unit_cost": 513,  # $0201
        "exit_unit_in_uncleared_stages": True,
        "wily_4_requirement_type": "weapons",
        "wily_4_wily_stages": 2,
        "wily_4_robot_masters": 6,
        "wily_4_weapons": 5,
        "skip_intro_stage": True,
        "skip_robot_museum": True,
        "robot_museum_robot_masters": 7,
    }

    def test_custom_rom_config_order(self) -> None:
        config = get_rom_config(self.world)

        self.assertEqual(len(config), MM7_ROM_CONFIG_SIZE)

        self.assertEqual(
            config,
            bytes([
                7,      # Starting lives
                1,      # Starting E-Tanks
                2,      # Starting W-Tanks
                1,      # Starting S-Tanks
                0x2A,   # Starting bolts low
                0x02,   # Starting bolts high
                1,      # Paid Exit Unit
                0x01,   # Paid Exit Unit cost low
                0x02,   # Paid Exit Unit cost high
                1,      # Exit Unit in uncleared stages
                2,      # Wily 4 requirement type: weapons
                2,      # Wily stages required
                6,      # Robot Masters required for Wily 4
                5,      # Weapons required for Wily 4
                1,      # Skip Intro Stage
                1,      # Skip Robot Museum
                7,      # Robot Masters required for Robot Museum
            ]),
        )