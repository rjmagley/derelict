from __future__ import annotations

from typing import List

import random

from .base_item import BaseItem
from . import WeaponType

class BaseWeapon(BaseItem):

    def __init__(self, die_count: int = 1, damage_die: int = 1, hands: int = 1, weapon_types: List[WeaponType] = [], **kwargs):
        super().__init__(**kwargs)

        self.die_count = die_count
        self.damage_die = damage_die
        self.hands = hands
        self._weapon_types = weapon_types

    # if weapon only has one type, return that type
    # otherwise, return the type that best matches the skill of the player
    @property
    def weapon_type(self) -> WeaponType:
        if len(self._weapon_types) == 1:
            return self._weapon_types[0]
        else:
            # if there's more than one type
            # really weapons should have a max of like two types
            # but who knows what horrible thing the future holds


            player = self.engine.player
            stats = [(t, player.player_stats[t]) for t in self._weapon_types]
            # gross lambda to sort by the player stat
            # [-1] gets the last item from the list
            # the final [0] gets the type of the weapon
            return sorted(stats, key=lambda t: t[1])[-1][0]

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