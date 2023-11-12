from __future__ import annotations

from typing import TYPE_CHECKING

from . import MOVE_KEYS, WAIT_KEYS, CURSOR_Y_KEYS, CONFIRM_KEYS, ESCAPE_KEYS

import tcod

if TYPE_CHECKING:
    from game_engine import GameEngine
    
from .event_handler import EventHandler
from input_handlers.handler_types import HandlerType



# this really doesn't do much at the moment!

class LookEventHandler(EventHandler):

    def __init__(self, engine: GameEngine):
        super().__init__(engine)
        self.x = self.engine.player.x
        self.y = self.engine.player.y
        self.handler_type = HandlerType.LOOK

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        key = event.sym

        if key in MOVE_KEYS and self.engine.map.in_bounds(self.x, self.y):
            self.x += MOVE_KEYS[key][0]
            self.y += MOVE_KEYS[key][1]

        if key in ESCAPE_KEYS:
            self.engine.switch_handler(HandlerType.GAME)