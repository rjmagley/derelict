from __future__ import annotations

import random

from typing import TYPE_CHECKING

from . import WeaponType, AmmunitionType, ReloadType, WeaponName
from .ranged_physical_weapon import RangedPhysicalWeapon
from .ranged_energy_weapon import RangedEnergyWeapon
from .melee_weapon import MeleeWeapon

from .weapon_properties import property_cqb, property_heavy_caliber, property_long_long_gun, property_light_bolt, property_belt_feeder

import random

if TYPE_CHECKING:
    from .base_weapon import BaseWeapon

# rare weapons are defined here - weapons that have a special name and can
# generate with different properties that modify the weapon's stats or functionality
# each weapon has a "pool" of properties, because not all properties make sense for all
# weapons - it's very Destiny 2 in this regard

rare_weapons = [WeaponName.HOLD_THAT_THOUGHT]

def get_rare_weapon() -> BaseWeapon:
    match random.choice(rare_weapons):
        case WeaponName.MEDIUM_IRON:
            weapon_stats = {'damage_die': 6, 'die_count': 3, 'magazine_size': 6, 'burst_count': 1, 'weapon_types': [WeaponType.PISTOL], 'name': 'Medium Iron', 'hands': 1, 'ammunition_size': 10, 'ammunition_type': AmmunitionType.HEAVY, 'optimal_range': 6, 'range_interval': 5, 'accuracy_bonus': 2, 'properties': [random.choice([property_cqb, property_heavy_caliber])]}
            test_weapon = RangedPhysicalWeapon(**weapon_stats)

        case WeaponName.HOLD_THAT_THOUGHT:
            weapon_stats = {'damage_die': 4, 'die_count': 4, 'magazine_size': 20, 'burst_count': 4, 'weapon_types': [WeaponType.SMG], 'name': 'Hold That Thought', 'hands': 1, 'ammunition_size': 16, 'ammunition_type': AmmunitionType.LIGHT, 'optimal_range': 5, 'range_interval': 5, 'accuracy_bonus': 0, 'properties': [random.choice([property_long_long_gun, property_light_bolt, property_belt_feeder])]}
            test_weapon = RangedPhysicalWeapon(**weapon_stats)

    test_weapon.apply_weapon_properties()
    return test_weapon