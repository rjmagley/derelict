from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Tuple, Any, Dict

import random

import color
from actions import ActionResult
from .base_weapon import BaseWeapon
from . import WeaponType, AmmunitionType, ReloadType, RangedWeaponProperty

from entities.player import Player


if TYPE_CHECKING:

    from magazine import Magazine
    from entities.enemy import Enemy

class RangedWeapon(BaseWeapon):
    def __init__(self, magazine_size: int = 6, burst_count: int = 1, ammunition_size: int = 10, ammunition_type: AmmunitionType = AmmunitionType.LIGHT, reload_type: ReloadType = ReloadType.STANDARD, properties: Dict[RangedWeaponProperty, Any] = {}, owner: Optional[Enemy | Player] = None, **kwargs):
        super().__init__(**kwargs)
        self.burst_count = burst_count
        self.ammunition_type = ammunition_type
        self.ammunition_size = ammunition_size
        self.char = '{'
        self.reload_type = reload_type
        match reload_type:
            case ReloadType.STANDARD:
                self.magazine_size = magazine_size
                self.loaded_ammo = magazine_size
                self.reload = self.standard_reload
            case ReloadType.SINGLE:
                self.magazine_size = magazine_size
                self.loaded_ammo = magazine_size
                self.reload = self.single_reload
            case ReloadType.BELT:
                self.fire = self.belt_fire
                self.magazine_size = 0
                self.loaded_ammo = 0
                self.reload = self.belt_reload

        self.properties = properties

        self.owner = owner

        

    # returns true if the weapon can fire and false if it can't (empty,
    # disabled, etc)
    @property
    def can_fire(self) -> bool:
        if self.reload_type == ReloadType.BELT:
            return (self.owner.magazine.get_current_ammo(self.ammunition_type) >
            self.ammunition_size * self.burst_count)
        return self.loaded_ammo != 0
        


    @property
    def status_string(self) -> str:
        status = f"{self.name} - {self.die_count}d{self.damage_die}x{self.burst_count}"
        return status

    @property
    def ammo_status(self) -> str:
        if self.reload_type == ReloadType.BELT:
            return f"{self.owner.magazine.get_percentage(self.ammunition_type)}%"
        return f"{self.loaded_ammo}/{self.magazine_size}"

    def fire(self) -> int:
        total_damage = 0
        burst = min(self.burst_count, self.loaded_ammo)
        for x in range(0, burst):
            total_damage += self.roll_damage()
        self.loaded_ammo -= burst
        return total_damage

    def belt_fire(self) -> int:
        total_damage = 0
        for x in range(0, self.burst_count):
            total_damage += self.roll_damage()
        self.owner.magazine.spend_ammo(self.ammunition_type, self.ammunition_size * self.burst_count)
        return total_damage

    # considered doing subclasses for the reload types but am not sure something
    # can dynamically subclass
    # instead, all ranged weapons have all the reload methods - the one used is
    # selected by the reload_type

    # standard magazine reload - player reloads entire weapon in one go
    def standard_reload(self, owner: Enemy | Player) -> ActionResult:

        magazine: Magazine = owner.magazine

        # no need to reload if full
        if self.loaded_ammo >= self.magazine_size:
            return ActionResult(False, "Your weapon is already fully loaded.", color.light_gray)

        # determine how many units of ammo needed
        ammunition_needed = (self.magazine_size - self.loaded_ammo) * self.ammunition_size
        
        if magazine.get_current_ammo(self.ammunition_type) < self.ammunition_size:
            return ActionResult(False, "You don't have enough ammo to load even one round.", color.light_gray)

        # player has enough ammo to fully load magazine - no fancy math needed
        if magazine.get_current_ammo(self.ammunition_type) >= ammunition_needed:
            magazine.spend_ammo(self.ammunition_type, ammunition_needed)
            self.loaded_ammo = self.magazine_size
            if isinstance(owner, Player):
                return ActionResult(True, "You fully load your weapon.", color.white, 10)
            else:
                return ActionResult(True, f"The {owner.name} loads its weapon.", color.white, 10)

        # player cannot fully reload - need to do a partial
        else:
            ammunition_available = magazine.get_current_ammo(self.ammunition_type)

            ammunition_used = ammunition_available // self.ammunition_size
            self.loaded_ammo += ammunition_used
            magazine.spend_ammo(self.ammunition_type, ammunition_used * self.ammunition_size)
            if isinstance(owner, Player):
                return ActionResult(True, "You load as much ammo as you have.", color.white, 10)
            else:
                return ActionResult(True, f"The {owner.name} loads as much ammo as it has.", color.white, 10)

    # single reload - player reloads one round at a time
    def single_reload(self, owner: Enemy | Player) -> ActionResult:

        magazine: Magazine = owner.magazine

        # no need to reload if full
        if self.loaded_ammo >= self.magazine_size:
            return ActionResult(False, "Your weapon is already fully loaded.", color.light_gray)

        elif magazine.get_current_ammo(self.ammunition_type) < self.ammunition_size:
            return ActionResult(False, "You don't have enough ammo to load even one round.", color.light_gray)

        else:
            magazine.spend_ammo(self.ammunition_type, self.ammunition_size)
            self.loaded_ammo += 1
            return ActionResult(True, f"You load a round into the {self.name}.", color.white, 5)

    def belt_reload(self, owner: Enemy | Player) -> ActionResult:

        return ActionResult(False, "This weapon automatically loads.", color.light_gray)


def place_random_ranged_weapon(x: int, y: int, map = None) -> RangedWeapon:
    weapon_choices = [
        {'damage_die': 4, 'die_count': 2, 'magazine_size': 10, 'burst_count': 2, 'weapon_types': [WeaponType.PISTOL], 'name': 'Burst Pistol', 'hands': 1, 'ammunition_size': 10, 'ammunition_type': AmmunitionType.LIGHT},
        {'damage_die': 3, 'die_count': 2, 'magazine_size': 24, 'burst_count': 3, 'weapon_types': [WeaponType.SMG], 'name': 'Light SMG', 'hands': 1, 'ammunition_size': 10, 'ammunition_type': AmmunitionType.LIGHT},
        {'damage_die': 4, 'die_count': 6, 'magazine_size': 5, 'burst_count': 1, 'weapon_types': [WeaponType.RIFLE], 'name': 'Heavy Repeater', 'hands': 2, 'ammunition_size': 12, 'ammunition_type': AmmunitionType.HEAVY},
        {'damage_die': 3, 'die_count': 7, 'magazine_size': 5, 'burst_count': 1, 'weapon_types': [WeaponType.SHOTGUN], 'name': 'Shotgun', 'hands': 2, 'ammunition_size': 14, 'ammunition_type': AmmunitionType.HEAVY, 'reload_type': ReloadType.SINGLE},
        {'damage_die': 2, 'die_count': 5, 'magazine_size': 12, 'burst_count': 3, 'weapon_types': [WeaponType.SHOTGUN, WeaponType.SMG], 'name': 'Weird Test Hybrid', 'hands': 2, 'ammunition_size': 14, 'ammunition_type': AmmunitionType.HEAVY, 'reload_type': ReloadType.SINGLE}
    ]

    weapon_stats = random.choice(weapon_choices)

    return RangedWeapon(x=x, y=y, map=map, **weapon_stats)

def get_test_belt_weapon(x: int, y: int, map = None):
    return RangedWeapon(x=x, y=y, map=map, **{'damage_die': 5, 'die_count': 4, 'magazine_size': 10, 'burst_count': 2, 'weapon_types': [WeaponType.RIFLE], 'name': 'Heavy Autogun', 'hands': 1, 'ammunition_size': 10, 'ammunition_type': AmmunitionType.LIGHT, 'reload_type': ReloadType.BELT, 'properties': {}})
