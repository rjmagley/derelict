from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from string import ascii_uppercase

from . import MOVE_KEYS, WAIT_KEYS, CURSOR_Y_KEYS, CONFIRM_KEYS, ESCAPE_KEYS

import tcod

from actions.actions import Action

if TYPE_CHECKING:
    from game_engine import GameEngine
    
from .event_handler import EventHandler
from . import game_event_handler
from . import view_item_event_handler

from input_handlers.handler_types import HandlerType

class InventoryViewEventHandler(EventHandler):

    def __init__(self, engine: GameEngine):
        super().__init__(engine)
        self.handler_type = HandlerType.INVENTORY_VIEW
        self.weapons_inventory = engine.player.inventory.weapons
        self.armor_inventory = engine.player.inventory.armor

        self.characters_available = [c for c in ascii_uppercase]
        self.all_keys = []

        self.weapons_keys = self.characters_available[0:len(self.weapons_inventory)]
        self.all_keys.extend(self.weapons_keys)
        self.weapons_dictionary = {k: i for k, i in zip(self.weapons_keys, self.weapons_inventory)}
        self.characters_available = self.characters_available[len(self.weapons_inventory):]

        print(self.characters_available)

        self.armor_keys = self.characters_available[0:len(self.armor_inventory)]
        self.all_keys.extend(self.armor_keys)
        self.armor_dictionary = {k: i for k, i in zip(self.armor_keys, self.armor_inventory)}
        self.characters_available = self.characters_available[len(self.armor_inventory)-1:-1]

        

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        player = self.engine.player
        key = event.sym

        # this will be extended with armor, consumables, etc.
        # at this point, the player's inventory doesn't Have any of that stuff
        # we'll get bnack to this
        if key.label in self.all_keys:
            match key.label:
                case key.label if key.label in self.weapons_dictionary.keys():
                    self.engine.switch_handler(HandlerType.ITEM_VIEW, item=self.weapons_dictionary[key.label])

        if key in ESCAPE_KEYS:
            self.engine.switch_handler(HandlerType.GAME)