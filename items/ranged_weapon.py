import random

from .base_item import BaseItem

from enum import auto, StrEnum

class WeaponType(StrEnum):
    PISTOL = "pistol"


class RangedWeapon(BaseItem):
    def __init__(self, damage_die: int = 1, die_count: int = 1, magazine_size: int = 6, burst_count: int = 1, **kwargs):
        super().__init__(**kwargs)
        self.magazine_size = magazine_size
        self.burst_count = burst_count
        self.loaded_ammo = magazine_size

    # returns true if the weapon can fire and false if it can't (empty,
    # disabled, etc)
    def fire(self) -> bool:
        if self.loaded_ammo < self.burst_count:
            return False
        self.loaded_ammo -= self.burst_count
        return True

class PistolWeapon(RangedWeapon):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.weapon_type = WeaponType.PISTOL
