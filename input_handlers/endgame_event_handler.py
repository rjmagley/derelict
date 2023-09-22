from __future__ import annotations

from . import MOVE_KEYS, WAIT_KEYS, CURSOR_Y_KEYS, CONFIRM_KEYS, ESCAPE_KEYS

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions.actions import Action, EscapeAction, BumpAction, WaitAction
from .event_handler import EventHandler

if TYPE_CHECKING:
    from game_engine import GameEngine

from input_handlers.handler_types import HandlerType

class EndgameEventHandler(EventHandler):

    def __init__(self, engine: GameEngine):
        super().__init__(engine)
        self.handler_type = HandlerType.ENDGAME

    def handle_events(self) -> None:
        for e in tcod.event.wait():
            action = self.dispatch(e)

            if action is None:
                continue

            action.perform()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None
        key = event.sym

        if key in ESCAPE_KEYS:
            action = EscapeAction(self.engine.player)

        # No valid key was pressed
        return action