from __future__ import annotations

from typing import Type

from enum import auto, StrEnum

from random import randint

from items.base_weapon import BaseWeapon

from actions import ActionResult

from .combatant import Combatant
from items.melee_weapon import MeleeWeapon
from items.ranged_weapon import RangedWeapon
from items import WeaponType, AmmunitionType

# from input_handlers.endgame_event_handler import EndgameEventHandler

from .inventory import Inventory

import color

class Skill(StrEnum):
    DUALWIELD = "dual-wielding"

# Player - the player character, moved by the player, etc.
class Player(Combatant):

    def __init__(self, **kwargs):
        super().__init__(name = "Player", blocks_movement = True, **kwargs)
        self.inventory = Inventory()
        # weapons held by the player
        # some weapons take up both hands - those are considered to be in the
        # "right" hand
        self.right_hand = None
        self.left_hand = None
        # ammunition is a dictionary representing the four ammunition types
        # ammunition is stored as a number from 0 to the player's max ammo
        # (starts at 1000) and rendered as a percentage on the UI
        self.max_light_ammo = 1000
        self.max_heavy_ammo = 1000
        self.max_explosive_ammo = 1000
        self.max_exotic_ammo = 1000
        self.ammunition = {
            AmmunitionType.LIGHT: 1000,
            AmmunitionType.HEAVY: 1000,
            AmmunitionType.EXPLOSIVE: 1000,
            AmmunitionType.EXOTIC: 1000
        }
        self.player_stats = {
            WeaponType.PISTOL: 10,
            WeaponType.RIFLE: 10,
            WeaponType.SMG: 10,
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

    @property
    def hp(self) -> int:
        return self._hp

    @property
    def is_alive(self) -> bool:
        return self._hp > 0

    @property
    def barehanded(self) -> bool:
        return self.right_hand == None and self.left_hand == None

    @property
    def twohanded_weapon(self) -> bool:
        if self.right_hand == None:
            return False
        else:
            return self.right_hand.hands == 2

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp <= 0:
            # self.engine.switch_handler(EndgameEventHandler)
            self.die()

    # returns true if equipping was successful, false otherwise
    # currently constantly returns True because there's no reason for equipping
    # to fail, but there may be in the future
    def equip_right_hand(self, weapon: BaseWeapon) -> bool:
        if weapon.hands == 1:
            self.right_hand = weapon
        else:
            self.left_hand = None
            self.right_hand = weapon
        return True

    def equip_left_hand(self, weapon: BaseWeapon) -> bool:
        if weapon.hands == 1:
            self.left_hand = weapon
        else:
            # two-handed weapons take up both hands
            self.left_hand = None
            self.right_hand = weapon
        return True

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

    # for now, just a fairly high chance to hit
    # will be modified later by player/enemy stats
    def ranged_attack(self, target: Combatant, weapon: RangedWeapon) -> ActionResult:
        damage = weapon.fire()
        if randint(1, 10) > 3:
            message = f"You hit the {target.name} for {damage} damage."
            target.take_damage(damage)
            return ActionResult(True, message, color.white, 10)
        else:
            return ActionResult(True, f"You miss the {target.name}.", color.light_gray, 10)

    # gonna call this every 10 auts to do things like player shield recharge,
    # ticking down status effects, etc. 
    def periodic_refresh(self):
        pass