from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions.actions import Action, EscapeAction, BumpAction, WaitAction
from input_handlers.handler_types import HandlerType

if TYPE_CHECKING:
    from game_engine import GameEngine

class EventHandler(tcod.event.EventDispatch[Action]):

    def __init__(self, engine: GameEngine):
        self.engine = engine
        self.handler_type = None

    def handle_events(self) -> None:
        for e in tcod.event.wait():
            action = self.dispatch(e)

            if action is None:
                continue

            # action should be something that takes a player's turn -
            # if a handler returns an action, something is happening
            if action.perform():

                self.engine.handle_enemy_actions()
                self.engine.update_fov()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()