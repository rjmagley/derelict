from __future__ import annotations

from . import MOVE_KEYS, WAIT_KEYS, CURSOR_Y_KEYS, CONFIRM_KEYS, ESCAPE_KEYS

from typing import Optional, TYPE_CHECKING

import tcod.event
import color

if TYPE_CHECKING:
    from game_engine import GameEngine

from .event_handler import EventHandler

class IntroEventHandler(EventHandler):

    def __init__(self):
        super().__init__(None)

    def ev_keydown(self, event: tcod.event.KeyDown):

        key = event.sym

        return key