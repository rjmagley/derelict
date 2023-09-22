from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Type
from string import ascii_uppercase

from . import MOVE_KEYS, WAIT_KEYS, CURSOR_Y_KEYS, CONFIRM_KEYS, ESCAPE_KEYS

import tcod

if TYPE_CHECKING:
    from game_engine import GameEngine
    from items.base_item import BaseItem
    
from .event_handler import EventHandler
from input_handlers.handler_types import HandlerType


class ViewItemEventHandler(EventHandler):
    def __init__(self, engine: GameEngine, item: Type[BaseItem]):
        super().__init__(engine)
        self.handler_type = HandlerType.ITEM_VIEW
        self.item = item

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        player = self.engine.player
        key = event.sym

        if key in ESCAPE_KEYS:
            self.engine.switch_handler(HandlerType.INVENTORY_VIEW)