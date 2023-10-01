from __future__ import annotations

from . import MOVE_KEYS, WAIT_KEYS, CURSOR_Y_KEYS, CONFIRM_KEYS, ESCAPE_KEYS

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions import ActionResult
from actions.actions import Action, EscapeAction, BumpAction, WaitAction, PickupItemAction, PlayerReloadAction

if TYPE_CHECKING:
    from game_engine import GameEngine

from .event_handler import EventHandler

from input_handlers.handler_types import HandlerType
from items.ranged_weapon import RangedWeapon
from items.ranged_energy_weapon import RangedEnergyWeapon

class GameEventHandler(EventHandler):

    def __init__(self, engine: GameEngine):
        super().__init__(engine)
        self.handler_type = HandlerType.GAME

    def ev_keydown(self, event: tcod.event.KeyDown) -> ActionResult:
        action = ActionResult(False)
        player = self.engine.player

        key, mod = event.sym, event.mod

        print(key.label)

        match key:
            case key if key in MOVE_KEYS:
                dx, dy = MOVE_KEYS[key]
                action = BumpAction(player, dx, dy).perform()
            case key if key in WAIT_KEYS:
                print("waiting")
                action = WaitAction(player).perform()

            case key if key in ESCAPE_KEYS:
                action = EscapeAction(player)

            case tcod.event.KeySym.g:
                action = PickupItemAction(player).perform()

            case tcod.event.KeySym.i:
                self.engine.switch_handler(HandlerType.INVENTORY_VIEW)

            case tcod.event.KeySym.x:
                self.engine.switch_handler(HandlerType.LOOK)

            case tcod.event.KeySym.r:
                weapon = player.right_hand
                action = PlayerReloadAction(player, weapon).perform()

            case tcod.event.KeySym.f:
                if isinstance(player.right_hand, RangedWeapon) or isinstance(player.right_hand, RangedEnergyWeapon):
                    self.engine.switch_handler(HandlerType.TARGETING, weapon=player.right_hand)
                else:
                    return ActionResult(False, "You don't have a ranged weapon in hand.")
                

            case tcod.event.KeySym.N5 if event.mod & tcod.event.KMOD_SHIFT:
                self.engine.switch_handler(HandlerType.CHARACTER_PROFILE)

            case tcod.event.KeySym.p if event.mod & tcod.event.KMOD_CTRL:
                self.engine.switch_handler(HandlerType.MESSAGE_HISTORY)
                

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
        print(action)
        return action