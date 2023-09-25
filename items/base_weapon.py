from __future__ import annotations

from typing import Set

import random

from .base_item import BaseItem
from . import WeaponType

class BaseWeapon(BaseItem):

    def __init__(self, damage_die: int = 1, die_count: int = 1, hands: int = 1, is_shoulder: bool = False, weapon_types: Set[WeaponType] = set(), **kwargs):
        super().__init__(**kwargs)
        self.damage_die = damage_die
        self.die_count = die_count
        self.hands = hands
        self.is_shoulder = is_shoulder
        self.weapon_types = weapon_types

    @property
    def status_string(self) -> str:
        return f"{self.name} - {self.die_count}d{self.damage_die}"

    @property
    def ammo_status(self) -> str:
        return ""

    def roll_damage(self):
        damage = 0
        for i in range(0, self.die_count):
            damage += random.randint(1, self.damage_die)

        return damage