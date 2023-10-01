from __future__ import annotations

from typing import Optional

from . import ArmorType
from .base_item import BaseItem

class BaseArmor(BaseItem):

    def __init__(self, armor_type: ArmorType, armor_points: int = 5, damage_resist: int = 0, name: Optional[str] = None, **kwargs):
        if name == None:
            match armor_type:
                case ArmorType.HELMET:
                    name = "Basic Helmet"
                case ArmorType.TORSO:
                    name = "Basic Chestplate"
                case ArmorType.ARMS:
                    name = "Basic Vambraces"
                case ArmorType.LEGS:
                    name = "Basic Greaves"
                case ArmorType.BACKPACK:
                    name = "Basic Backpack"
        super().__init__(name=name, char="[", **kwargs)
        self.max_armor_points = armor_points
        self.damage_resist = damage_resist
        self.armor_type = armor_type
        # properties is where various buffs will hang out
        # for now, just an empty dictionary
        self.properties = {}