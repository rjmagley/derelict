from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Tuple

import random

import color
from actions import ActionResult
from .ranged_weapon import RangedWeapon
from . import WeaponType, AmmunitionType, ReloadType


if TYPE_CHECKING:
    from entities.player import Player
    from magazine import Magazine

# energy weapons don't reload or have a lot of the other behavior other ranged
# weapons do - hence having their own class
# in the future it'll probably be wiser to do multiple inheritance? maybe?
class RangedEnergyWeapon(RangedWeapon):

    def __init__(self, charge_needed: int = 10, **kwargs):
        super().__init__(**kwargs)
        self.charge_needed = charge_needed
        self._weapon_types = [WeaponType.ENERGY]

    @property
    def status_string(self) -> str:
        return f"{self.name} - {'Ready' if self.can_fire else 'Not Ready'}"

    @property
    def ammo_status(self) -> str:
        return ""


    @property
    def can_fire(self) -> bool:
        return self.owner.energy_points >= self.charge_needed

    def fire(self, **kwargs) -> int:
        total_damage = 0
        for x in range(0, self.burst_count):
            total_damage += self.roll_damage()
        self.owner.energy_points -= self.charge_needed
        return total_damage

    def reload(self, player) -> ActionResult:
        return ActionResult(False, "This weapon can't be reloaded.", color.light_gray)