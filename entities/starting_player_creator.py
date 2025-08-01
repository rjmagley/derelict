from __future__ import annotations

from typing import TYPE_CHECKING

from decimal import Decimal

from .player import Player
from items.base_armor import BaseArmor
from items.ranged_energy_weapon import RangedEnergyWeapon
from items.ranged_recharge_weapon import RangedRechargeWeapon
from items.ranged_physical_weapon import RangedPhysicalWeapon
from items.melee_weapon import MeleeWeapon

from items.rare_weapons import get_rare_weapon

from items import WeaponType, AmmunitionType, ArmorType, ArmorProperty,ReloadType

from powers import PowerSkill

from powers.alacrity import AlacrityPower

def generate_player(class_name: str):

    player = Player(x=None, y=None, char='@')

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
            player.player_stats[PowerSkill.OFFENSE] = 15
            player.player_stats[PowerSkill.DEFENSE] = 15
            player.player_stats[PowerSkill.MANIPULATION] = 15
            player.player_stats[PowerSkill.ENHANCE] = 15
            starting_pistol = RangedPhysicalWeapon(die_count=2, damage_die=6, magazine_size=8, burst_count=1, weapon_types=[WeaponType.PISTOL], name='heavy pistol', hands=1, ammunition_size=12, ammunition_type=AmmunitionType.LIGHT, minimum_range=5,
            maximum_range=10, range_interval=3)
            starting_sword = MeleeWeapon(die_count=3, damage_die=5, weapon_types=[WeaponType.SWORD], name='longsword', hands=1)
            starting_rifle = RangedPhysicalWeapon(die_count=3, damage_die=5, magazine_size=36, burst_count=3, weapon_types=[WeaponType.RIFLE], name='burst rifle', hands=2, ammunition_size=15, ammunition_type=AmmunitionType.LIGHT, minimum_range=8,
            maximum_range=22, range_interval=5)

            player.inventory.insert_item(starting_rifle)
            player.inventory.insert_item(starting_pistol)
            player.inventory.insert_item(starting_sword)

            player.equip_right_hand(starting_pistol)
            player.equip_left_hand(starting_sword)
            

        case 'bulwark':
            player.class_name = 'Bulwark'
            player.player_stats[WeaponType.PISTOL] = 15
            player.player_stats[WeaponType.RIFLE] = 15
            player.player_stats[WeaponType.SMG] = 15
            player.player_stats[WeaponType.SHOTGUN] = 15
            player.player_stats[WeaponType.LAUNCHER] = 15
            player.player_stats[WeaponType.SMG] = 15
            player.player_stats[WeaponType.HEAVY] = 15

            player.player_stats[PowerSkill.OFFENSE] = 12
            player.player_stats[PowerSkill.DEFENSE] = 12
            player.player_stats[PowerSkill.MANIPULATION] = 8
            player.player_stats[PowerSkill.ENHANCE] = 8

            starting_rifle = RangedPhysicalWeapon(die_count=3, damage_die=6, magazine_size=20, burst_count=2, weapon_types=[WeaponType.RIFLE], name='heavy burster', hands=2, ammunition_size=20, ammunition_type=AmmunitionType.HEAVY, minimum_range=9,
            maximum_range=22, range_interval=6)
            starting_shotgun = RangedPhysicalWeapon(die_count=7, damage_die=3, magazine_size=10, burst_count=1, weapon_types=[WeaponType.SHOTGUN], name='light shotgun', hands=2, ammunition_size=20, ammunition_type=AmmunitionType.LIGHT, minimum_range=5,
            maximum_range=11, range_interval=3, reload_type=ReloadType.SINGLE)
            starting_shoulder = RangedEnergyWeapon(damage_die=4, die_count=6, charge_needed=25, burst_count=1, radius=1, minimum_range=7,
            maximum_range=34, range_interval=7, is_shoulder=True, weapon_types=[WeaponType.HEAVY, WeaponType.ENERGY], name='laser cannon')

            player.inventory.insert_item(starting_shotgun)
            player.inventory.insert_item(starting_rifle)
            player.inventory.insert_item(starting_shoulder)

            player.equip_right_hand(starting_rifle)
            player.equip_right_shoulder(starting_shoulder)

        case 'ranger':

            player.player_stats[WeaponType.PISTOL] = 14
            player.player_stats[WeaponType.RIFLE] = 16
            player.player_stats[WeaponType.SMG] = 10
            player.player_stats[WeaponType.SHOTGUN] = 12
            player.player_stats[WeaponType.LAUNCHER] = 10
            player.player_stats[WeaponType.SMG] = 10
            player.player_stats[WeaponType.HEAVY] = 8

            player.player_stats[PowerSkill.OFFENSE] = 12
            player.player_stats[PowerSkill.DEFENSE] = 10
            player.player_stats[PowerSkill.MANIPULATION] = 14
            player.player_stats[PowerSkill.ENHANCE] = 14

            player.class_name = 'Ranger'
            starting_rifle = RangedRechargeWeapon(damage_die=8, die_count=3, burst_count=1, weapon_types=[WeaponType.RIFLE], name='recharge rifle', hands=2, minimum_range=10,
            maximum_range=25, range_interval=5)
            starting_pistol = RangedPhysicalWeapon(damage_die=6, die_count=2, magazine_size=8, burst_count=1, weapon_types=[WeaponType.PISTOL], name='heavy pistol', hands=1, ammunition_size=12, ammunition_type=AmmunitionType.LIGHT, minimum_range=5,
            maximum_range=14, range_interval=3)
            starting_axe = MeleeWeapon(die_count=4, damage_die=5, weapon_types=[WeaponType.AXE], name='war axe', hands=1)

            player.inventory.insert_item(starting_pistol)
            player.inventory.insert_item(starting_axe)
            player.inventory.insert_item(starting_rifle)

            player.equip_right_hand(starting_rifle)

            player.powers.append(AlacrityPower(caster = player))
            

        case 'test':
            player.class_name = 'Test'
            player.player_stats[WeaponType.PISTOL] = 16
            player.player_stats[WeaponType.RIFLE] = 16
            player.player_stats[WeaponType.SMG] = 12
            player.player_stats[WeaponType.SWORD] = 16
            player.player_stats[WeaponType.AXE] = 14
            player.player_stats[WeaponType.POLEARM] = 12
            player.player_stats[WeaponType.BLUNT] = 12
            player.player_stats[WeaponType.SHIELD] = 12
            
            starting_pistol = get_rare_weapon()
            player.inventory.insert_item(starting_pistol)
            player.equip_right_hand(starting_pistol)
            

            player.helmet.properties[ArmorProperty.BASE_SHIELD] = 500
            

    return player