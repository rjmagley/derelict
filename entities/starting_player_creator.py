from __future__ import annotations

from typing import TYPE_CHECKING

from decimal import Decimal

from .player import Player
from items.base_armor import BaseArmor
from items.ranged_energy_weapon import RangedEnergyWeapon
from items.ranged_recharge_weapon import RangedRechargeWeapon
from items.ranged_physical_weapon import RangedPhysicalWeapon
from items.melee_weapon import MeleeWeapon

from items import WeaponType, AmmunitionType, ArmorType, ArmorProperty,ReloadType

def generate_player(class_name: str):

    player = Player(x=None, y=None, char='@')

    player.helmet = BaseArmor(armor_type = ArmorType.HELMET, properties = {ArmorProperty.BASE_ARMOR: 10})
    player.chest = BaseArmor(armor_type = ArmorType.TORSO, properties = {ArmorProperty.BASE_ARMOR: 10, ArmorProperty.DAMAGE_RESISTANCE: 3})
    player.arms = BaseArmor(armor_type = ArmorType.ARMS, properties = {ArmorProperty.BASE_ARMOR: 10})
    player.legs = BaseArmor(armor_type = ArmorType.LEGS, properties = {ArmorProperty.BASE_ARMOR: 10})
    player.backpack = BaseArmor(armor_type = ArmorType.BACKPACK, properties = {ArmorProperty.BASE_ARMOR: 10, ArmorProperty.ENERGY_CAPACITY: 50, ArmorProperty.ENERGY_REGENERATION: Decimal(10.0)})
    player.shield_generator = BaseArmor(armor_type = ArmorType.SHIELD_GENERATOR, properties = {ArmorProperty.BASE_SHIELD: 10, ArmorProperty.SHIELD_REBOOT_TIME: 5, ArmorProperty.SHIELD_REGENERATION: Decimal(15.0)})

    match class_name:
        case 'noble':
            player.class_name = 'Noble'
            player.player_stats[WeaponType.PISTOL] = 16
            player.player_stats[WeaponType.RIFLE] = 14
            player.player_stats[WeaponType.SMG] = 14
            player.player_stats[WeaponType.SWORD] = 16
            player.player_stats[WeaponType.AXE] = 14
            player.player_stats[WeaponType.POLEARM] = 14
            player.player_stats[WeaponType.BLUNT] = 14
            player.player_stats[WeaponType.SHIELD] = 14
            starting_pistol = RangedPhysicalWeapon(die_count=2, damage_die=6, magazine_size=8, burst_count=1, weapon_types=[WeaponType.PISTOL], name='heavy pistol', hands=1, ammunition_size=12, ammunition_type=AmmunitionType.LIGHT, optimal_range=8, range_interval=3)
            starting_sword = MeleeWeapon(die_count=3, damage_die=5, weapon_types=[WeaponType.SWORD], name='longsword', hands=1)
            starting_rifle = RangedPhysicalWeapon(die_count=3, damage_die=5, magazine_size=36, burst_count=3, weapon_types=[WeaponType.RIFLE], name='burst rifle', hands=2, ammunition_size=15, ammunition_type=AmmunitionType.LIGHT, optimal_range=10, range_interval=5)

            player.equip_right_hand(starting_pistol)
            player.equip_left_hand(starting_sword)
            player.inventory.items.append(starting_rifle)

        case 'bulwark':
            player.class_name = 'Bulwark'
            player.player_stats[WeaponType.PISTOL] = 15
            player.player_stats[WeaponType.RIFLE] = 15
            player.player_stats[WeaponType.SMG] = 15
            player.player_stats[WeaponType.SHOTGUN] = 15
            player.player_stats[WeaponType.LAUNCHER] = 15
            player.player_stats[WeaponType.SMG] = 15
            player.player_stats[WeaponType.HEAVY] = 15

            starting_rifle = RangedPhysicalWeapon(die_count=3, damage_die=6, magazine_size=20, burst_count=2, weapon_types=[WeaponType.RIFLE], name='heavy burster', hands=2, ammunition_size=20, ammunition_type=AmmunitionType.HEAVY, optimal_range=8, range_interval=6)
            starting_shotgun = RangedPhysicalWeapon(die_count=7, damage_die=3, magazine_size=10, burst_count=1, weapon_types=[WeaponType.SHOTGUN], name='light shotgun', hands=2, ammunition_size=20, ammunition_type=AmmunitionType.LIGHT, optimal_range=6, range_interval=3, reload_type=ReloadType.SINGLE)
            starting_shoulder = None

            player.equip_right_hand(starting_rifle)
            player.inventory.items.append(starting_shotgun)

        case 'ranger':
            player.class_name = 'Ranger'
            starting_rifle = RangedRechargeWeapon(damage_die=8, die_count=3, burst_count=1, weapon_types=[WeaponType.RIFLE], name='recharge rifle', hands=2, optimal_range=10, range_interval=5)
            starting_pistol = RangedPhysicalWeapon(damage_die=6, die_count=2, magazine_size=8, burst_count=1, weapon_types=[WeaponType.PISTOL], name='heavy pistol', hands=1, ammunition_size=12, ammunition_type=AmmunitionType.LIGHT, optimal_range=8, range_interval=3)
            starting_axe = MeleeWeapon(die_count=4, damage_die=5, weapon_types=[WeaponType.AXE], name='war axe', hands=1)

            player.equip_right_hand(starting_rifle)
            player.inventory.items.append(starting_pistol)
            player.inventory.items.append(starting_axe)
            

    return player