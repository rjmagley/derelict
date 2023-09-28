from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from string import ascii_uppercase

from . import MOVE_KEYS, WAIT_KEYS, CURSOR_Y_KEYS, CONFIRM_KEYS, ESCAPE_KEYS

import tcod

if TYPE_CHECKING:
    from game_engine import GameEngine
    
from .event_handler import EventHandler
from . import game_event_handler
from . import view_item_event_handler

from input_handlers.handler_types import HandlerType

class CharacterProfileEventHandler(EventHandler):

    def __init__(self, engine: GameEngine):
        super().__init__(engine)
        self.handler_type = HandlerType.CHARACTER_PROFILE

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        key = event.sym

        if key in ESCAPE_KEYS:
            self.engine.switch_handler(HandlerType.GAME)