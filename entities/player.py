from __future__ import annotations

from typing import Type, List, Optional

from decimal import Decimal

from enum import auto, StrEnum

from random import randint

from render_order import RenderOrder
from items.base_weapon import BaseWeapon

from actions import ActionResult

from .mover import Mover
from items.melee_weapon import MeleeWeapon
from items.ranged_weapon import RangedWeapon
from items import WeaponType, AmmunitionType, ArmorType

from die_rollers import player_attack_roll

# from input_handlers.endgame_event_handler import EndgameEventHandler

from items.inventory import Inventory
from items.magazine import Magazine
from items.shield_generator import ShieldGenerator
from items.base_armor import BaseArmor

import color

class Skill(StrEnum):
    DUALWIELD = "dual-wielding"

# Player - the player character, moved by the player, etc.
class Player(Mover):

    def __init__(self, **kwargs):
        
        self.render_order = RenderOrder.COMBATANT

        # the player's inventory - handles things held by the player
        # things equipped by the player are different
        self.inventory = Inventory()

        # the player's magazine is where their ammo is stored/created/etc.
        self.magazine = Magazine()

        # shield generator controls shield stuff
        self.shield_generator = ShieldGenerator()

        # these five represent all the player's armor
        self.helmet = BaseArmor(armor_type = ArmorType.HELMET)
        self.chest = BaseArmor(armor_type = ArmorType.TORSO)
        self.arms = BaseArmor(armor_type = ArmorType.ARMS)
        self.legs = BaseArmor(armor_type = ArmorType.LEGS)
        self.backpack = BaseArmor(armor_type = ArmorType.BACKPACK)


        # weapons held by the player, in hands/on shoulders
        # some weapons take up both hands - those are considered to be in the
        # "right" hand
        self.right_hand = None
        self.left_hand = None
        self.right_shoulder = None
        self.left_shoulder = None

        # ammunition is a dictionary representing the four ammunition types
        # ammunition is stored as a number from 0 to the player's max ammo
        # (starts at 1000) and rendered as a percentage on the UI
        
        self.player_stats = {
            WeaponType.PISTOL: 10,
            WeaponType.RIFLE: 18,
            WeaponType.SMG: 14,
            WeaponType.SHOTGUN: 10,
            WeaponType.LAUNCHER: 10,
            WeaponType.HEAVY: 10,
            WeaponType.ENERGY: 10,
            WeaponType.SWORD: 10,
            WeaponType.AXE: 10,
            WeaponType.POLEARM: 10,
            WeaponType.BLUNT: 10,
            WeaponType.SHIELD: 10,
            Skill.DUALWIELD: 10
        }

        self.armor_points = self.max_armor

        super().__init__(name = "Player", blocks_movement = True, **kwargs)


    @property
    def max_armor(self) -> int:
        return sum([a.max_armor_points for a in self.armor])

    # @max_armor.setter
    # def max_armor(self, value) -> None:
    #     self.max_armor = sum([a.max_armor_points for a in self.armor])

    @property
    def armor(self) -> List[BaseArmor]:
        return [self.helmet, self.chest, self.arms, self.legs, self.backpack]

    @property
    def hp(self) -> int:
        return self.armor_points

    @hp.setter
    def hp(self, value: int) -> None:
        self.armor_points -= value
        if self.armor_points <= 0:
            self.die()

    @property
    def shield(self) -> int:
        return self.shield_generator.current_shield

    @property
    def is_alive(self) -> bool:
        return self.armor_points > 0

    @property
    def barehanded(self) -> bool:
        return self.right_hand == None and self.left_hand == None

    @property
    def twohanded_weapon(self) -> bool:
        if self.right_hand == None:
            return False
        else:
            return self.right_hand.hands == 2

    @property
    def equipped_weapons(self) -> List[Optional[BaseWeapon]]:
        return [self.right_hand, self.left_hand, self.right_shoulder, self.left_shoulder]

    @property
    def defense(self) -> int:
        return sum([a.damage_resist for a in self.armor])

    # the player's HP setter is a bit messier than normal - players have
    # shields, then armor, then a few states before death
    def take_damage(self, value: int) -> None:
        print(f"receiving {value} damage, shield is currently {self.shield}")
        remaining_damage = self.shield_generator.take_damage(value)
        if remaining_damage > 0:
            print(f"player taking {value} damage")
            self.armor_points -= value
            if self.armor_points <= 0:
                print("player died")
                # self.engine.switch_handler(EndgameEventHandler)
                self.die()

    def has_equipped(self, item: BaseWeapon):
        return item is self.right_hand or item is self.left_hand

    # returns true if equipping was successful, false otherwise
    # currently constantly returns True because there's no reason for equipping
    # to fail, but there may be in the future
    def equip_right_hand(self, weapon: BaseWeapon) -> ActionResult:
        if weapon.hands == 1:
            self.right_hand = weapon
        else:
            self.left_hand = None
            self.right_hand = weapon
        return ActionResult(True, f"You equip the {weapon.name}.", color.white, 10)

    # eventually this should probably become "equip_offhand" or something
    def equip_left_hand(self, weapon: BaseWeapon) -> ActionResult:
        if self.twohanded_weapon:
            return ActionResult(False, f"Both your hands are full.", color.light_gray)
        if weapon.hands == 1:
            self.left_hand = weapon
            return ActionResult(True, f"You equip the {weapon.name} in your off hand.", color.white, 10)
        else:
            return ActionResult(False, f"The {weapon.name} is too big for your offhand.", color.light_gray)

    def die(self) -> None:
        print("You died!")

    def attack(self, target: Combatant):
        damage = 0
        if self.barehanded:
            damage = self.power - target.defense
            output_string = f"You attack {target.name} barehanded "
            if damage > 0:
                output_string += f"for {damage} damage."
            else:
                output_string += "for no damage."
            self.engine.message_log.add_message(output_string)
            target.hp -= damage
        else:
            # god this is gonna need a lot of logic to figure out melee vs.
            # ranged - probably split into a few different functions
            if self.right_hand:
                damage = self.right_hand.roll_damage() - target.defense
                output_string = f"You attack {target.name} with your {self.right_hand.name} "
                if damage > 0:
                    output_string += f"for {damage} damage."
                else:
                    output_string += "for no damage."
                self.engine.message_log.add_message(output_string)
                target.hp -= damage


    def ranged_attack(self, target: Combatant, weapon: RangedWeapon) -> ActionResult:
        damage = weapon.fire()
        if player_attack_roll(weapon, self):
            message = f"You hit the {target.name} for {damage} damage."
            target.take_damage(damage)
            return ActionResult(True, message, color.white, 10)
        else:
            return ActionResult(True, f"You miss the {target.name}.", color.light_gray, 10)



    # gonna call this every 10 auts to do things like player shield recharge,
    # ticking down status effects, etc. 
    def periodic_refresh(self):
        self.shield_generator.regeneration()
        pass