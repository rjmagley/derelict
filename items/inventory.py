from __future__ import annotations

from typing import TYPE_CHECKING, Type

from .base_weapon import BaseWeapon
from .base_armor import BaseArmor

if TYPE_CHECKING:
    from .base_item import BaseItem

class Inventory():

    def __init__(self):
        self.weapons = []
        self.armor = []
        self.consumables = []
        self.artifacts = []

    # @property
    # def all_items(self):
    #     all_items = []
    #     for l in [self.weapons, self.armor, self.consumables, self.artifacts]:
    #         all_items.extend(l)
    #     return all_items

    # returns True if an item of this type can fit in the inventory,
    # False otherwise
    def space_remaining(self, item: BaseItem) -> bool:
        match item:
            case BaseWeapon():
                print(len(self.weapons))
                return len(self.weapons) <= 4
            case BaseArmor():
                return len(self.armor) <= 4

    def insert_item(self, item: BaseItem) -> None:
        match item:
            case BaseWeapon():
                self.weapons.append(item)
            case BaseArmor():
                self.weapons.append(item)
