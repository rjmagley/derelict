from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Tuple, Any, Dict, List

import random
import math

import color
from actions import ActionResult
from .base_weapon import BaseWeapon
from . import WeaponType, AmmunitionType, ReloadType




if TYPE_CHECKING:
    from magazine import Magazine
    from entities.player import Player
    from entities.enemy import Enemy
    from entities.base_entity import BaseEntity
    from .weapon_properties import WeaponProperty


class RangedWeapon(BaseWeapon):
    def __init__(self, burst_count: int = 1, properties: List[WeaponProperty] = [], radius: int = 1, optimal_range: int = 7, range_interval: int = 7, is_shoulder: bool = False, fire_time: int=10, accuracy_bonus: int=0, **kwargs):
        super().__init__(**kwargs)
        self.burst_count = burst_count
        self.char = '{'
        self.properties = properties
        
        self.radius = radius
        self.is_shoulder = is_shoulder

        # the optimal range is the range at which the weapon has no penalties -
        # from optimal range to optimal range * 2
        # if you're closer or further from the enemy, you get a -1 for each
        # range interval of distance between you (rounded up)
        # essentially, the higher the range interval, the better the weapon
        # performs out-of-range
        # 
        # at some point I should change this to a minimum-maximum range rather
        # than just multiplying the value by 2, but I got other things to do
        self.optimal_range = optimal_range
        self.range_interval = range_interval

        self.fire_time = fire_time
        self.accuracy_bonus = accuracy_bonus

        # if properties != []:
        #     for p in properties:
        #         p.modify_weapon(self)

    @property
    def can_fire(self) -> bool:
        return False

    @property
    def status_string(self) -> str:
        return f"{self.ammo_status} - {self.die_string}"

    @property
    def die_string(self) -> str:
        return f"{self.die_count}d{self.damage_die}{'x'+str(self.burst_count) if self.burst_count > 1 else ''}"

    @property
    def ammo_status(self) -> str:
        return ""

    def fire(self, **kwargs) -> int:
        raise NotImplementedError

    def belt_fire(self) -> int:
        raise NotImplementedError

    def reload(self, owner: Enemy | Player) -> ActionResult:
        raise NotImplementedError

    def calculate_distance_modifier(self, entity_a: BaseEntity, entity_b: BaseEntity) -> int:
        distance = math.ceil(entity_a.distance(entity_b))
        if distance in range(self.optimal_range, (2*self.optimal_range)+1):
            return 0
        elif distance < self.optimal_range:
            return  math.ceil((self.optimal_range - distance) // self.range_interval)
        else:
            return  math.ceil((distance - self.optimal_range * 2) // self.range_interval)