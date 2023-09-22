import random

from .base_weapon import BaseWeapon

from enum import auto, StrEnum

class WeaponType(StrEnum):
    PISTOL = "pistol"


class RangedWeapon(BaseWeapon):
    def __init__(self, magazine_size: int = 6, burst_count: int = 1, **kwargs):
        super().__init__(**kwargs)
        self.magazine_size = magazine_size
        self.burst_count = burst_count
        self.loaded_ammo = magazine_size
        print(self.damage_die)

    # returns true if the weapon can fire and false if it can't (empty,
    # disabled, etc)
    def fire(self) -> bool:
        if self.loaded_ammo < self.burst_count:
            return False
        self.loaded_ammo -= self.burst_count
        return True

    @property
    def status_string(self) -> str:
        status = f"{self.name} - {self.die_count}d{self.damage_die}x{self.burst_count}"
        return status

    @property
    def ammo_status(self) -> str:
        return f"{self.loaded_ammo}/{self.magazine_size}"

class PistolWeapon(RangedWeapon):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.weapon_type = WeaponType.PISTOL
