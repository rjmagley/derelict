from __future__ import annotations

from . import MOVE_KEYS, WAIT_KEYS, CURSOR_Y_KEYS, CONFIRM_KEYS, ESCAPE_KEYS

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions import ActionResult
from actions.actions import Action, EscapeAction, BumpAction, WaitAction, PickupItemAction, PlayerReloadAction
import tile_types
import color

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

        print(key, mod)


        match key:
            case key if key in MOVE_KEYS:
                dx, dy = MOVE_KEYS[key]
                action = BumpAction(player, dx, dy).perform()

            case key if key in WAIT_KEYS and not event.mod:
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

            # shift-r to bring up aux weapon reloader?
            # or do we want that for special weapon reloads - in which case, we
            # should use ctrl-r

            case tcod.event.KeySym.c:
                self.engine.switch_handler(HandlerType.POWER_LIST)

            # shift-t to bring up the offhand/shoulder weapon targeter
            case tcod.event.KeySym.t if event.mod & tcod.event.KMOD_SHIFT:
                if player.left_hand == None and player.right_shoulder == None and player.left_shoulder == None:
                    return ActionResult(False, "You have no auxillary weapons to fire.")
                self.engine.switch_handler(HandlerType.WEAPON_SELECT)

            case tcod.event.KeySym.f:
                if isinstance(player.right_hand, RangedWeapon):
                    self.engine.switch_handler(HandlerType.TARGETING, weapon=player.right_hand)
                else:
                    return ActionResult(False, "You don't have a ranged weapon in hand.")
                

            case tcod.event.KeySym.N5 if event.mod & tcod.event.KMOD_SHIFT:
                self.engine.switch_handler(HandlerType.CHARACTER_PROFILE)

            case tcod.event.KeySym.p if event.mod & tcod.event.KMOD_CTRL:
                self.engine.switch_handler(HandlerType.MESSAGE_HISTORY)

            case tcod.event.KeySym.PERIOD if event.mod & tcod.event.KMOD_SHIFT:
                if self.engine.map.tiles[player.x, player.y] == tile_types.down_stairs:
                    self.engine.advance_map()
                    return ActionResult(False, "You descend...", color.yellow)
                else:
                    return ActionResult(False, "There's no place to go down here.")

                
                

        return action