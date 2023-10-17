from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Tuple, Any, Dict

import random
import math

import color
from actions import ActionResult
from .base_weapon import BaseWeapon
from . import WeaponType, AmmunitionType, ReloadType, RangedWeaponProperty




if TYPE_CHECKING:
    from magazine import Magazine
    from entities.player import Player
    from entities.enemy import Enemy
    from entities.base_entity import BaseEntity

class RangedWeapon(BaseWeapon):
    def __init__(self, burst_count: int = 1, properties: Dict[RangedWeaponProperty, Any] = {},radius: int = 1, optimal_range: int = 7, range_interval: int = 7, is_shoulder: bool = False, **kwargs):
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
        # essentially, the hither the range interval, the better the weapon
        # performs out-of-range
        self.optimal_range = optimal_range
        self.range_interval = range_interval

    @property
    def can_fire(self) -> bool:
        return False

    @property
    def status_string(self) -> str:
        raise NotImplementedError

    @property
    def ammo_status(self) -> str:
        raise NotImplementedError

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