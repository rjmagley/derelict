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

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        player = self.engine.player
        key = event.sym

        inventory_keys = ascii_uppercase[0:len(player.inventory.items)]
        inventory_items = {k: i for k, i in zip(inventory_keys, player.inventory.items)}

        if key.label in inventory_keys:
            self.engine.switch_handler(HandlerType.ITEM_VIEW, item=inventory_items[key.label])

        if key in ESCAPE_KEYS:
            self.engine.switch_handler(HandlerType.GAME)