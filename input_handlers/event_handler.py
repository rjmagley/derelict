from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions import ActionResult

from actions.actions import Action, EscapeAction, BumpAction, WaitAction
from input_handlers.handler_types import HandlerType

if TYPE_CHECKING:
    from game_engine import GameEngine

class EventHandler(tcod.event.EventDispatch[Action]):

    def __init__(self, engine: GameEngine):
        self.engine = engine
        self.handler_type = None

    def handle_events(self) -> ActionResult:
        for e in tcod.event.wait():
            action_result = self.dispatch(e)

            # if action_result.message != None:
            #     self.engine.add_message(action_result.message, action_result.message_color)

            return action_result


    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()