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
    def __init__(self, burst_count: int = 1, properties: List[WeaponProperty] = [], radius: int = 1, minimum_range: int = 7, maximum_range: int = 14, range_interval: int = 7, is_shoulder: bool = False, fire_time: int=10, accuracy_bonus: int=0, **kwargs):
        super().__init__(**kwargs)
        self.burst_count = burst_count
        self.char = '{'
        self.properties = properties
        
        self.radius = radius
        self.is_shoulder = is_shoulder

        # weapons have a minimum and maximum range where being outside of those
        # ranges start giving you range interval penalties
        self.minimum_range = minimum_range
        self.maximum_range = maximum_range
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
        if distance in range(self.minimum_range, self.maximum_range+1):
            return 0
        elif distance < self.minimum_range:
            return  math.ceil((self.minimum_range - distance) // self.range_interval)
        else:
            return  math.ceil((distance - self.maximum_range) // self.range_interval)

    # returns True if the target distance is within the weapon's range band
    # and false otherwise
    # permissable_error is an optional argument - if provided, the function
    # will still return True if the distance modifier is less than the
    # argument
    # some enemies want to fire as much as possible, some want to make sure
    # that they're at the appropriate range
    def weapon_in_range(self, entity_a: BaseEntity, entity_b: BaseEntity, 
        permissable_error: int = 0):

        return self.calculate_distance_modifier(entity_a, entity_b) <= permissable_error
