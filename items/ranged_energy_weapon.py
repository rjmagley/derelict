from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Tuple

import random

import color
from actions import ActionResult
from .base_weapon import BaseWeapon
from . import WeaponType, AmmunitionType, ReloadType


if TYPE_CHECKING:
    from entities.player import Player
    from magazine import Magazine

# energy weapons don't reload or have a lot of the other behavior other ranged
# weapons do - hence having their own class
# in the future it'll probably be wiser to do multiple inheritance? maybe?
class RangedEnergyWeapon(BaseWeapon):

    def __init__(self, charge_needed: int = 10, burst_count: int = 1, **kwargs):
        super().__init__(**kwargs)
        self.charge_needed = charge_needed
        self._weapon_types = [WeaponType.ENERGY]
        self.burst_count = burst_count

    @property
    def status_string(self) -> str:
        return f"{self.name} - {'Ready' if self.can_fire else 'Not Ready'}"

    @property
    def can_fire(self) -> bool:
        return self.engine.player.energy_points >= self.charge_needed

    def fire(self) -> int:
        total_damage = 0
        for x in range(0, self.burst_count):
            total_damage += self.roll_damage()
        self.engine.player.energy_points -= self.charge_needed
        return total_damage

    def reload(self, player) -> ActionResult:
        return ActionResult(False, "This weapon can't be reloaded.", color.light_gray)

def get_test_energy_weapon():
    return RangedEnergyWeapon(name="Energy Rifle", charge_needed = 10, burst_count = 3, damage_die = 3, die_count = 3, hands = 2)