from random import randint

from .combatant import Combatant
from items.melee_weapon import MeleeWeapon
from items.ranged_weapon import RangedWeapon

# from input_handlers.endgame_event_handler import EndgameEventHandler

from .inventory import Inventory

import color

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
            'light': 1000,
            'heavy': 1000,
            'explosive': 1000,
            'exotic': 1000
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

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp <= 0:
            # self.engine.switch_handler(EndgameEventHandler)
            self.die()

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
    def ranged_attack(self, target: Combatant, weapon: RangedWeapon):
        damage = weapon.fire()
        if randint(1, 10) > 7:
            self.engine.add_message(f"You hit the {target.name} for {damage} damage.")
            target.take_damage(damage)
        else:
            self.engine.add_message(f"You miss the {target.name}.", color.light_gray)