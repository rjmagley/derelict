from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Tuple

import random

import color
from actions import ActionResult
from .ranged_weapon import RangedWeapon
from .ranged_energy_weapon import RangedEnergyWeapon
from . import WeaponType, AmmunitionType, ReloadType


if TYPE_CHECKING:
    from entities.player import Player
    from magazine import Magazine

class RangedRechargeWeapon(RangedEnergyWeapon):

    def __init__(self, charge_needed: int = 10, max_charge: int = 20, recharge_rate: int = 2, **kwargs):
        super().__init__(**kwargs)
        self.max_charge = max_charge
        self.charge_needed = charge_needed
        self.current_charge = max_charge
        self.recharge_rate = recharge_rate
        self._weapon_types.append(WeaponType.ENERGY)

    @property
    def can_fire(self) -> bool:
        return self.current_charge >= self.charge_needed

    @property
    def ammo_status(self) -> str:
        return f"{self.current_charge}/{self.max_charge}"

    def fire(self, **kwargs) -> int:
        total_damage = 0
        for x in range(0, self.burst_count):
            total_damage += self.roll_damage()
        self.current_charge -= self.charge_needed
        return total_damage

    def recharge(self) -> None:
        self.current_charge = min(self.current_charge + self.recharge_rate, self.max_charge)

