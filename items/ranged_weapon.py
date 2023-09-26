from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Tuple

import random

from .base_weapon import BaseWeapon
from . import WeaponType, AmmunitionType

if TYPE_CHECKING:
    from entities.player import Player


class RangedWeapon(BaseWeapon):
    def __init__(self, magazine_size: int = 6, burst_count: int = 1, ammunition_size: int = 10, ammunition_type: AmmunitionType = AmmunitionType.LIGHT, **kwargs):
        super().__init__(**kwargs)
        self.magazine_size = magazine_size
        self.burst_count = burst_count
        self.loaded_ammo = magazine_size
        self.ammunition_type = ammunition_type
        self.ammunition_size = ammunition_size
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

    # returns true if the reload is successful and false otherwise
    # there may be a scenario where reloads are a little different from weapon
    # to weapon - single-shell loading, for example. or energy weapons, which
    # don't reload? we may have a future where ranged weapons need to inherit
    # from multiple classes - hand vs. aux weapons, reload types, etc.

    # what a nightmare
    def reload(self, player: Player) -> tuple[bool, str]:

        # no need to reload if full
        if self.loaded_ammo >= self.magazine_size:
            return (False, "Your weapon is fully loaded.")

        # determine how many units of ammo needed
        ammunition_needed = (self.magazine_size - self.loaded_ammo) * self.ammunition_size
        
        if player.ammunition[self.ammunition_type] < self.ammunition_size:
            return (False, "You don't have enough ammo to load even one round.")

        # player has enough ammo to fully load magazine - no fancy math needed
        if player.ammunition[self.ammunition_type] >= ammunition_needed:
            player.ammunition[self.ammunition_type] -= ammunition_needed
            self.loaded_ammo = self.magazine_size
            return (True, "You fully load your weapon.")

        # player cannot fully reload - need to do a partial
        else:
            ammunition_available = player.ammunition[self.ammunition_type] - ammunition_needed

            ammunition_used = ammunition_available // self.ammunition_size
            self.loaded_ammo += ammunition_used
            player.ammunition[self.ammunition_type] -= ammunition_used * self.ammunition_size
            return (True, "You load as much ammo as you have.")



def place_random_ranged_weapon(x: int, y: int) -> RangedWeapon:
    weapon_choices = [
        {'damage_die': 4, 'die_count': 2, 'magazine_size': 10, 'burst_count': 2, 'weapon_types': {WeaponType.PISTOL}, 'name': 'Burst Pistol', 'hands': 1},
        {'damage_die': 3, 'die_count': 2, 'magazine_size': 24, 'burst_count': 3, 'weapon_types': {WeaponType.SMG}, 'name': 'Light SMG', 'hands': 1},
        {'damage_die': 4, 'die_count': 6, 'magazine_size': 5, 'burst_count': 1, 'weapon_types': {WeaponType.RIFLE}, 'name': 'Heavy Repeater', 'hands': 2},
        {'damage_die': 3, 'die_count': 7, 'magazine_size': 5, 'burst_count': 1, 'weapon_types': {WeaponType.SHOTGUN}, 'name': 'Shotgun', 'hands': 2},
    ]

    weapon_stats = random.choice(weapon_choices)

    return RangedWeapon(x=x, y=y, **weapon_stats)
