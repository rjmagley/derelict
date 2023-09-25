import random

from .base_weapon import BaseWeapon
from . import WeaponType


class RangedWeapon(BaseWeapon):
    def __init__(self, magazine_size: int = 6, burst_count: int = 1, **kwargs):
        super().__init__(**kwargs)
        self.magazine_size = magazine_size
        self.burst_count = burst_count
        self.loaded_ammo = magazine_size
        self.char = '{'

    # returns true if the weapon can fire and false if it can't (empty,
    # disabled, etc)
    @property
    def can_fire(self) -> bool:
        return self.loaded_ammo != 0

    @property
    def status_string(self) -> str:
        status = f"{self.name} - {self.die_count}d{self.damage_die}x{self.burst_count}"
        return status

    @property
    def ammo_status(self) -> str:
        return f"{self.loaded_ammo}/{self.magazine_size}"

    def fire(self) -> int:
        total_damage = 0
        burst = min(self.burst_count, self.loaded_ammo)
        for x in range(0, burst):
            total_damage += self.roll_damage()
        self.loaded_ammo -= burst
        return total_damage

def place_random_ranged_weapon(x: int, y: int) -> RangedWeapon:
    weapon_choices = [
        {'damage_die': 4, 'die_count': 2, 'magazine_size': 10, 'burst_count': 2, 'weapon_types': {WeaponType.PISTOL}, 'name': 'Burst Pistol', 'hands': 1},
        {'damage_die': 3, 'die_count': 2, 'magazine_size': 24, 'burst_count': 3, 'weapon_types': {WeaponType.SMG}, 'name': 'Light SMG', 'hands': 1},
        {'damage_die': 4, 'die_count': 6, 'magazine_size': 5, 'burst_count': 1, 'weapon_types': {WeaponType.RIFLE}, 'name': 'Heavy Repeater', 'hands': 2},
        {'damage_die': 7, 'die_count': 3, 'magazine_size': 5, 'burst_count': 1, 'weapon_types': {WeaponType.SHOTGUN}, 'name': 'Shotgun', 'hands': 1},
    ]

    weapon_stats = random.choice(weapon_choices)

    return RangedWeapon(x=x, y=y, **weapon_stats)
