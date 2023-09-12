from . import MOVE_KEYS, WAIT_KEYS, CURSOR_Y_KEYS, CONFIRM_KEYS, ESCAPE_KEYS

from typing import Optional

import tcod.event

from actions.actions import Action, EscapeAction, MovementAction

class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = MovementAction(dx, dy)

        elif key in ESCAPE_KEYS:
            action = EscapeAction()

        # No valid key was pressed
        return action