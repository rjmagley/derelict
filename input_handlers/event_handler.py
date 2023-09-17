from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions.actions import Action, EscapeAction, BumpAction, WaitAction

if TYPE_CHECKING:
    from game_engine import GameEngine

class EventHandler(tcod.event.EventDispatch[Action]):

    def __init__(self, engine: GameEngine):
        self.engine = engine

    def handle_events(self) -> None:
        raise NotImplementedError()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()