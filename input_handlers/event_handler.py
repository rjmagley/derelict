from . import MOVE_KEYS, WAIT_KEYS, CURSOR_Y_KEYS, CONFIRM_KEYS, ESCAPE_KEYS

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions.actions import Action, EscapeAction, BumpAction

if TYPE_CHECKING:
    from game_engine import GameEngine

class EventHandler(tcod.event.EventDispatch[Action]):

    def __init__(self, engine):
        self.engine = engine

    def handle_events(self) -> None:
        for e in tcod.event.wait():
            action = self.dispatch(e)

            if action is None:
                continue

            action.perform()

            self.engine.handle_enemy_actions()
            self.engine.update_fov()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None
        player = self.engine.player
        key = event.sym

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = BumpAction(player, dx, dy)

        elif key in ESCAPE_KEYS:
            action = EscapeAction(player)

        # No valid key was pressed
        return action