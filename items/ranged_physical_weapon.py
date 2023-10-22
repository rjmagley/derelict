from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Tuple, Any, Dict

import random

import color
from actions import ActionResult
from .ranged_weapon import RangedWeapon
from . import WeaponType, AmmunitionType, ReloadType, RangedWeaponProperty

from entities.player import Player


if TYPE_CHECKING:

    from magazine import Magazine
    from entities.enemy import Enemy

class RangedPhysicalWeapon(RangedWeapon):
    def __init__(self, magazine_size: int = 6, burst_count: int = 1, ammunition_size: int = 10, ammunition_type: AmmunitionType = AmmunitionType.LIGHT, reload_type: ReloadType = ReloadType.STANDARD, properties: Dict[RangedWeaponProperty, Any] = {}, owner: Optional[Enemy | Player] = None, radius: int = 1, reload_time: int=10, **kwargs):
        super().__init__(**kwargs)
        self.burst_count = burst_count
        self.ammunition_type = ammunition_type
        self.ammunition_size = ammunition_size
        
        self.char = '{'
        self.reload_type = reload_type
        self.reload_time = reload_time

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
        self.radius = radius

        

    # returns true if the weapon can fire and false if it can't (empty,
    # disabled, etc)
    @property
    def can_fire(self) -> bool:
        if self.reload_type == ReloadType.BELT:
            return (self.owner.magazine.get_current_ammo(self.ammunition_type) >
            self.ammunition_size * self.burst_count)
        return self.loaded_ammo != 0
        


    @property
    def ammo_status(self) -> str:
        if self.reload_type == ReloadType.BELT:
            return f"{self.owner.magazine.get_percentage(self.ammunition_type)}%"
        return f"{self.loaded_ammo}/{self.magazine_size}"

    # this really needs a system where part of a weapon burst can misslo
    def fire(self, **kwargs) -> int:
        total_damage = 0
        burst = min(self.burst_count, self.loaded_ammo)
        for x in range(0, burst):
            total_damage += self.roll_damage()
        self.loaded_ammo -= burst
        return total_damage

    def belt_fire(self, **kwargs) -> int:
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
                return ActionResult(True, "You fully load your weapon.", color.white, self.reload_time)
            else:
                return ActionResult(True, f"The {owner.name} loads its weapon.", color.white, self.reload_time)

        # player cannot fully reload - need to do a partial
        else:
            ammunition_available = magazine.get_current_ammo(self.ammunition_type)

            ammunition_used = ammunition_available // self.ammunition_size
            self.loaded_ammo += ammunition_used
            magazine.spend_ammo(self.ammunition_type, ammunition_used * self.ammunition_size)
            if isinstance(owner, Player):
                return ActionResult(True, "You load as much ammo as you have.", color.white, self.reload_time)
            else:
                return ActionResult(True, f"The {owner.name} loads as much ammo as it has.", color.white, self.reload_time)

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
            return ActionResult(True, f"You load a round into the {self.name}.", color.white, self.reload_time)

    def belt_reload(self, owner: Enemy | Player) -> ActionResult:

        return ActionResult(False, "This weapon automatically loads.", color.light_gray)

    def apply_weapon_properties(self):
        if len(self.properties) != 0:
            for p in self.properties:
                p.modify_weapon(self)

        if self.reload_type != ReloadType.BELT:
            self.loaded_ammo = self.magazine_size
