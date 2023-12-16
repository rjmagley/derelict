from __future__ import annotations

from typing import TYPE_CHECKING

from . import CONFIRM_KEYS, INTERMISSION_KEYS

import tcod

if TYPE_CHECKING:
    from game_engine import GameEngine
    
from .event_handler import EventHandler
from input_handlers.handler_types import HandlerType
from items import ArmorType

# intermission handler - exists to let player swap between different items that
# can't be switched during normal gameplay - armor and shoulder weapons
# also lets you permanently discard weapons and armor so you can enter the next
# map with a cleaner inventory
class IntermissionEventHandler(EventHandler):

    def __init__(self, engine: GameEngine):
        super().__init__(engine)
        self.handler_type = HandlerType.INTERMISSION
        self.player = self.engine.player
        self.inventory = self.engine.player.inventory

        self.inventory_items = {
            'left_shoulder': [self.player.left_shoulder] + [w for w in self.inventory.weapons if w.is_shoulder],
            'right_shoulder': [self.player.right_shoulder] + [w for w in self.inventory.weapons if w.is_shoulder],
            'magazine': [self.player.magazine] + [m for m in self.inventory.armor if m.armor_type == ArmorType.MAGAZINE],
            'helmet': [self.player.helmet] + [a for a in self.inventory.armor if a.armor_type == ArmorType.HELMET],
            'chest': [self.player.chest] + [a for a in self.inventory.armor if a.armor_type == ArmorType.TORSO],
            'arms': [self.player.arms] + [a for a in self.inventory.armor if a.armor_type == ArmorType.ARMS],
            'legs': [self.player.legs] + [a for a in self.inventory.armor if a.armor_type == ArmorType.LEGS],
            'backpack': [self.player.backpack] + [a for a in self.inventory.armor if a.armor_type == ArmorType.BACKPACK],
            'shield': [self.player.shield_generator] + [a for a in self.inventory.armor if a.armor_type == ArmorType.SHIELD_GENERATOR],
        }

        self.chosen_items = {
            'left_shoulder': self.player.left_shoulder,
            'right_shoulder': self.player.right_shoulder,
            'magazine': self.player.magazine,
            'helmet': self.player.helmet,
            'chest': self.player.chest,
            'arms': self.player.arms,
            'legs': self.player.legs,
            'backpack': self.player.backpack,
            'shield': self.player.shield_generator, 
        }

        self.current_index = {
            'left_shoulder': 0,
            'right_shoulder': 0,
            'magazine': 0,
            'helmet': 0,
            'chest': 0,
            'arms': 0,
            'legs': 0,
            'backpack': 0,
            'shield': 0,    
        }

        self.items_to_drop = {
            'left_shoulder': [],
            'right_shoulder': [],
            'magazine': [],
            'helmet': [],
            'chest': [],
            'arms': [],
            'legs': [],
            'backpack': [],
            'shield': []
        }

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:

        key, mod = event.sym, event.mod

        # this will help us not have to write the worst possible statements
        # in the below match statement
        if key in INTERMISSION_KEYS:
            inventory_dict_key = INTERMISSION_KEYS[key]

            if not mod:
                self.current_index[inventory_dict_key] = (self.current_index[inventory_dict_key] + 1) % len(self.inventory_items[inventory_dict_key])

            # this needs some special code to make sure that a shoulder weapon
            # doesn't get equipped twice 
            elif mod & tcod.event.KMOD_SHIFT :
                chosen_index = self.current_index[inventory_dict_key]
                chosen_item = self.inventory_items[inventory_dict_key][chosen_index]
                self.chosen_items[inventory_dict_key] = chosen_item
                if chosen_item in self.items_to_drop[inventory_dict_key]:
                    self.items_to_drop[inventory_dict_key].remove(chosen_item)


            elif mod & tcod.event.KMOD_CTRL:
                chosen_index = self.current_index[inventory_dict_key]
                chosen_item = self.inventory_items[inventory_dict_key][chosen_index]

                # let's not let the player drop their only armor
                if chosen_item == self.chosen_items[inventory_dict_key]:
                    pass
                elif chosen_item in self.items_to_drop[inventory_dict_key]:
                    self.items_to_drop[inventory_dict_key].remove(chosen_item)
                else:
                    self.items_to_drop[inventory_dict_key].append(chosen_item)
