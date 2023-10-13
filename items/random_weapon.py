from __future__ import annotations

import random

from typing import TYPE_CHECKING

from . import WeaponType, AmmunitionType, ReloadType
from .ranged_physical_weapon import RangedPhysicalWeapon
from .ranged_energy_weapon import RangedEnergyWeapon

if TYPE_CHECKING:
    from .ranged_weapon import RangedWeapon


def place_random_ranged_weapon(x: int, y: int, map = None) -> RangedWeapon:
    physical_weapon_choices = [
        {'damage_die': 4, 'die_count': 2, 'magazine_size': 10, 'burst_count': 2, 'weapon_types': [WeaponType.PISTOL], 'name': 'Burst Pistol', 'hands': 1, 'ammunition_size': 10, 'ammunition_type': AmmunitionType.LIGHT, 'optimal_range': 6, 'range_interval': 4},
        {'damage_die': 3, 'die_count': 2, 'magazine_size': 24, 'burst_count': 3, 'weapon_types': [WeaponType.SMG], 'name': 'Light SMG', 'hands': 1, 'ammunition_size': 10, 'ammunition_type': AmmunitionType.LIGHT, 'optimal_range': 7, 'range_interval': 3},
        {'damage_die': 4, 'die_count': 6, 'magazine_size': 5, 'burst_count': 1, 'weapon_types': [WeaponType.RIFLE], 'name': 'Heavy Repeater', 'hands': 2, 'ammunition_size': 12, 'ammunition_type': AmmunitionType.HEAVY, 'optimal_range': 8, 'range_interval': 5},
        {'damage_die': 3, 'die_count': 7, 'magazine_size': 5, 'burst_count': 1, 'weapon_types': [WeaponType.SHOTGUN], 'name': 'Shotgun', 'hands': 2, 'ammunition_size': 14, 'ammunition_type': AmmunitionType.HEAVY, 'reload_type': ReloadType.SINGLE, 'optimal_range': 6, 'range_interval': 3},
        {'damage_die': 5, 'die_count': 4, 'magazine_size': 10, 'burst_count': 2, 'weapon_types': [WeaponType.RIFLE], 'name': 'Heavy Autogun', 'hands': 1, 'ammunition_size': 10, 'ammunition_type': AmmunitionType.LIGHT, 'reload_type': ReloadType.BELT, 'properties': {}, 'optimal_range': 5, 'range_interval': 7},
        {'damage_die': 4, 'die_count': 8, 'magazine_size': 6, 'burst_count': 3, 'weapon_types': [WeaponType.RIFLE, WeaponType.HEAVY], 'name': 'Light Autocannon', 'hands': 1, 'ammunition_size': 10, 'ammunition_type': AmmunitionType.HEAVY, 'reload_type': ReloadType.SINGLE, 'properties': {}, 'optimal_range': 9, 'range_interval': 4, 'is_shoulder': True}
    ]

    energy_weapon_choices = [
        {'name': 'Energy Rifle', 'charge_needed': 10, 'burst_count': 3, 'damage_die': 3, 'die_count': 3, 'hands': 2, 'optimal_range': 7, 'range_interval': 7}
    ]

    all_choices = physical_weapon_choices + energy_weapon_choices

    weapon_stats = random.choice(all_choices)

    if weapon_stats in physical_weapon_choices:
        return RangedPhysicalWeapon(x=x, y=y, map=map, **weapon_stats)

    elif weapon_stats in energy_weapon_choices:
        return RangedEnergyWeapon(x=x, y=y, map=map, **weapon_stats)

def place_random_shoulder_weapon(x: int, y: int, map = None) -> RangedWeapon:
    physical_weapon_choices = [
    {'damage_die': 4, 'die_count': 8, 'magazine_size': 6, 'burst_count': 3, 'weapon_types': [WeaponType.RIFLE, WeaponType.HEAVY], 'name': 'Light Autocannon', 'ammunition_size': 25, 'ammunition_type': AmmunitionType.HEAVY, 'reload_type': ReloadType.SINGLE, 'properties': {}, 'optimal_range': 9, 'range_interval': 4, 'is_shoulder': True}
    ]

    energy_weapon_choices = [

    ]

    all_choices = physical_weapon_choices + energy_weapon_choices

    weapon_stats = random.choice(all_choices)

    if weapon_stats in physical_weapon_choices:
        return RangedPhysicalWeapon(x=x, y=y, map=map, **weapon_stats)

    elif weapon_stats in energy_weapon_choices:
        return RangedEnergyWeapon(x=x, y=y, map=map, **weapon_stats)