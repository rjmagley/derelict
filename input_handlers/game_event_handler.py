from . import MOVE_KEYS, WAIT_KEYS, CURSOR_Y_KEYS, CONFIRM_KEYS, ESCAPE_KEYS, Handlers

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions.actions import Action, EscapeAction, BumpAction, WaitAction
from .event_handler import EventHandler

if TYPE_CHECKING:
    from game_engine import GameEngine

class GameEventHandler(EventHandler):

    def handle_events(self) -> None:
        for e in tcod.event.wait():
            action = self.dispatch(e)
            print(e)

            if action is None:
                continue

            action.perform()

            self.engine.handle_enemy_actions()
            self.engine.update_fov()


    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None
        player = self.engine.player
        key = event.sym

        print(event.mod)

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = BumpAction(player, dx, dy)

        elif key in WAIT_KEYS:
            print("waiting")
            action = WaitAction(player)

        elif key in ESCAPE_KEYS:
            action = EscapeAction(player)

        elif event.mod & tcod.event.KMOD_CTRL and key == tcod.event.KeySym.p:
            self.engine.switch_handler(Handlers.MESSAGE_HISTORY_HANDLER)

        # No valid key was pressed
        return action