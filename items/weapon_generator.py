from __future__ import annotations

import random

from typing import TYPE_CHECKING

from . import WeaponType, AmmunitionType, ReloadType, WeaponName
from .ranged_physical_weapon import RangedPhysicalWeapon
from .ranged_energy_weapon import RangedEnergyWeapon
from .melee_weapon import MeleeWeapon

if TYPE_CHECKING:
    from .base_weapon import BaseWeapon

common_weapons = [WeaponName.BURST_PISTOL, WeaponName.LIGHT_SMG,
    WeaponName.HEAVY_REPEATER, WeaponName.SHOTGUN, WeaponName.HEAVY_AUTOGUN,
    WeaponName.LIGHT_AUTOCANNON, WeaponName.ENERGY_RIFLE, WeaponName.LONGSWORD]

def place_random_common_weapon(x: int, y: int, map = None) -> BaseWeapon:
    # it would be really cool if these stats were defined in a .json file
    # rather than hardcoded here - could we create instances of these
    # and then copy them when necessary?
    match random.choice(common_weapons):
        case WeaponName.BURST_PISTOL:
            weapon_stats = {'damage_die': 4, 'die_count': 2, 'magazine_size': 10, 'burst_count': 2, 'weapon_types': [WeaponType.PISTOL], 'name': 'burst pistol', 'hands': 1, 'ammunition_size': 10, 'ammunition_type': AmmunitionType.LIGHT, 'minimum_range': 6, 'maximum_range': 12, 'range_interval': 4}
            return RangedPhysicalWeapon(x=x, y=y, map=map, **weapon_stats)
        case WeaponName.LIGHT_SMG:
            weapon_stats = {'damage_die': 3, 'die_count': 2, 'magazine_size': 24, 'burst_count': 3, 'weapon_types': [WeaponType.SMG], 'name': 'light SMG', 'hands': 1, 'ammunition_size': 10, 'ammunition_type': AmmunitionType.LIGHT, 'minimum_range': 5, 'maximum_range': 15, 'range_interval': 3}
            return RangedPhysicalWeapon(x=x, y=y, map=map, **weapon_stats)
        case WeaponName.HEAVY_REPEATER:
            weapon_stats = {'damage_die': 4, 'die_count': 6, 'magazine_size': 5, 'burst_count': 1, 'weapon_types': [WeaponType.RIFLE], 'name': 'heavy repeater', 'hands': 2, 'ammunition_size': 12, 'ammunition_type': AmmunitionType.HEAVY, 'minimum_range': 8, 'maximum_range': 32, 'range_interval': 5}
            return RangedPhysicalWeapon(x=x, y=y, map=map, **weapon_stats)
        case WeaponName.SHOTGUN:
            weapon_stats = {'damage_die': 3, 'die_count': 7, 'magazine_size': 5, 'burst_count': 1, 'weapon_types': [WeaponType.SHOTGUN], 'name': 'shotgun', 'hands': 2, 'ammunition_size': 14, 'ammunition_type': AmmunitionType.HEAVY, 'reload_type': ReloadType.SINGLE, 'minimum_range': 6, 'maximum_range': 12, 'range_interval': 3}
            return RangedPhysicalWeapon(x=x, y=y, map=map, **weapon_stats)
        case WeaponName.HEAVY_AUTOGUN:
            weapon_stats = {'damage_die': 5, 'die_count': 3, 'magazine_size': 10, 'burst_count': 3, 'weapon_types': [WeaponType.RIFLE], 'name': 'heavy autogun', 'hands': 1, 'ammunition_size': 10, 'ammunition_type': AmmunitionType.LIGHT, 'reload_type': ReloadType.BELT, 'properties': {}, 'minimum_range': 5, 'maximum_range': 20, 'range_interval': 7}
            return RangedPhysicalWeapon(x=x, y=y, map=map, **weapon_stats)
        case WeaponName.LIGHT_AUTOCANNON:
            weapon_stats = {'damage_die': 4, 'die_count': 8, 'magazine_size': 6, 'burst_count': 2, 'weapon_types': [WeaponType.RIFLE, WeaponType.HEAVY], 'name': 'light autocannon', 'hands': 1, 'ammunition_size': 10, 'ammunition_type': AmmunitionType.HEAVY, 'reload_type': ReloadType.SINGLE, 'properties': {}, 'minimum_range': 9, 'maximum_range': 27, 'range_interval': 4, 'is_shoulder': True}
            return RangedPhysicalWeapon(x=x, y=y, map=map, **weapon_stats)
        case WeaponName.ENERGY_RIFLE:
            weapon_stats = {'name': 'Energy Rifle', 'charge_needed': 10, 'burst_count': 3, 'damage_die': 3, 'die_count': 3, 'hands': 2, 'minimum_range': 5, 'maximum_range': 35, 'range_interval': 7}
            return RangedEnergyWeapon(x=x, y=y, map=map, **weapon_stats)
        case WeaponName.LONGSWORD:
            weapon_stats = {'die_count': 3, 'damage_die': 6, 'weapon_types': [WeaponType.SWORD], 'name': 'longsword', 'hands': 1}
            return MeleeWeapon(x=x, y=y, map=map, **weapon_stats)
