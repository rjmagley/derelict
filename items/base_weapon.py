from __future__ import annotations

from typing import List, TYPE_CHECKING, Optional

import random

from .base_item import BaseItem
from . import WeaponType

if TYPE_CHECKING:
    from entities.player import Player
    from entities.enemy import Enemy

class BaseWeapon(BaseItem):

    def __init__(self, die_count: int = 1, damage_die: int = 1, hands: int = 1, weapon_types: List[WeaponType] = [],  is_special = False, owner: Optional[Enemy | Player] = None,  properties: List[RangedWeaponProperty] = [], **kwargs):
        super().__init__(**kwargs)

        self.die_count = die_count
        self.damage_die = damage_die
        self.hands = hands
        self._weapon_types = weapon_types
        self.is_special = is_special
        self.owner = owner
        self.properties = properties
        self.is_shoulder = False


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
        return f"{self.die_string}"

    @property
    def die_string(self) -> str:
        return f"{self.damage_die}d{self.die_count}"

    @property
    def ammo_status(self) -> str:
        return ""

    def roll_damage(self):
        damage = 0
        print(f"rolling damage with {self.name}")
        for i in range(0, self.die_count):
            damage += random.randint(1, self.damage_die)

        return damage

    def apply_weapon_properties(self):
        if len(self.properties) != 0:
            for p in self.properties:
                p.modify_weapon(self)