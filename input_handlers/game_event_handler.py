from __future__ import annotations

from . import MOVE_KEYS, WAIT_KEYS, CURSOR_Y_KEYS, CONFIRM_KEYS, ESCAPE_KEYS

from . import message_history_handler, inventory_view_event_handler

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions.actions import Action, EscapeAction, BumpAction, WaitAction, PickupItemAction

if TYPE_CHECKING:
    from game_engine import GameEngine

from .event_handler import EventHandler

class GameEventHandler(EventHandler):

    def __init__(self, engine: GameEngine):
        super().__init__(engine)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None
        player = self.engine.player

        key, mod = event.sym, event.mod

        match key:
            case key if key in MOVE_KEYS:
                dx, dy = MOVE_KEYS[key]
                action = BumpAction(player, dx, dy)
            case key if key in WAIT_KEYS:
                print("waiting")
                action = WaitAction(player)

            case key if key in ESCAPE_KEYS:
                action = EscapeAction(player)

            case tcod.event.KeySym.g:
                action = PickupItemAction(player)

            case tcod.event.KeySym.i:
                self.engine.switch_handler(inventory_view_event_handler.InventoryViewEventHandler)

            case tcod.event.KeySym.p if event.mod & tcod.event.KMOD_CTRL:
                self.engine.switch_handler(message_history_handler.MessageHistoryHandler)
                

        # key = event.sym

        # if key in MOVE_KEYS:
        #     dx, dy = MOVE_KEYS[key]
        #     action = BumpAction(player, dx, dy)

        # elif key in WAIT_KEYS:
        #     print("waiting")
        #     action = WaitAction(player)

        # elif key in ESCAPE_KEYS:
        #     action = EscapeAction(player)

        # elif key == tcod.event.KeySym.g:
        #     action = PickupItemAction(player)

        # elif event.mod & tcod.event.KMOD_CTRL and key == tcod.event.KeySym.p:
        #     self.engine.switch_handler(message_history_handler.MessageHistoryHandler)

        # No valid key was pressed
        return action