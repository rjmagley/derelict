from __future__ import annotations

from typing import TYPE_CHECKING

from .base_weapon import BaseWeapon

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


    def insert_item(self, item: BaseItem):
        if isinstance(item, BaseWeapon):
            if len(self.weapons) < 5:
                self.weapons.append(item)
