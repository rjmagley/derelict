from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from . import MOVE_KEYS, WAIT_KEYS, CURSOR_Y_KEYS, CONFIRM_KEYS, ESCAPE_KEYS, Handlers

import tcod

if TYPE_CHECKING:
    from game_engine import GameEngine

from .event_handler import EventHandler


class MessageHistoryHandler(EventHandler):

    def __init__(self, engine: GameEngine):
        super().__init__(engine)

    def handle_events(self) -> None:
        for e in tcod.event.wait():
            action = self.dispatch(e)

            if action is None:
                continue

            action.perform()

    # there should be more here for like, scrolling through messages
    # I just don't want to deal with this right now

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        player = self.engine.player
        key = event.sym

        if key in ESCAPE_KEYS:
            self.engine.switch_handler(Handlers.GAME_EVENT_HANDLER)