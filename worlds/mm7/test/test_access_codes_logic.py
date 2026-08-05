from BaseClasses import CollectionState

from .. import names
from ..rules import can_buy_shop_upgrade
from .bases import MM7TestBase


class TestShopLogicWithAccessCodes(MM7TestBase):
    options = {
        "robot_master_access_codes": True,
    }

    def test_hyper_bolt_without_cloud_access_is_not_enough(self) -> None:
        state = CollectionState(self.multiworld)
        state.add_item(names.hyper_bolt, self.player)

        self.assertFalse(
            can_buy_shop_upgrade(state, self.world)
        )

    def test_hyper_bolt_and_cloud_access_allow_shop_upgrades(self) -> None:
        state = CollectionState(self.multiworld)
        state.add_item(names.hyper_bolt, self.player)
        state.add_item(names.cloud_man_access, self.player)
        self.assertTrue(
            can_buy_shop_upgrade(state, self.world)
        )

    def test_cloud_access_without_hyper_bolt_is_not_enough(self) -> None:
        state = CollectionState(self.multiworld)
        state.add_item(names.cloud_man_access, self.player)

        self.assertFalse(
            can_buy_shop_upgrade(state, self.world)
        )


class TestShopLogicWithoutAccessCodes(MM7TestBase):
    options = {
        "robot_master_access_codes": False,
    }

    def test_hyper_bolt_alone_allows_shop_upgrades(self) -> None:
        state = CollectionState(self.multiworld)
        state.add_item(names.hyper_bolt, self.player)

        self.assertTrue(
            can_buy_shop_upgrade(state, self.world)
        )