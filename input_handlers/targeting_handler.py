from __future__ import annotations

from typing import TYPE_CHECKING

from . import MOVE_KEYS, WAIT_KEYS, CURSOR_Y_KEYS, CONFIRM_KEYS, ESCAPE_KEYS

import tcod

from actions.actions import PlayerFireAction

if TYPE_CHECKING:
    from game_engine import GameEngine
    from items.ranged_weapon import RangedWeapon
    
from .look_event_handler import LookEventHandler
from input_handlers.handler_types import HandlerType

class TargetingEventHandler(LookEventHandler):

    def __init__(self, engine: GameEngine, weapon: RangedWeapon):
        super().__init__(engine)
        self.x = self.engine.player.x
        self.y = self.engine.player.y
        self.handler_type = HandlerType.TARGETING
        self.weapon = weapon
        self.player = self.engine.player

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        key = event.sym

        print("targeting keydown")
        match key:
            case key if key in MOVE_KEYS and self.engine.map.in_bounds(self.x, self.y):
                self.x += MOVE_KEYS[key][0]
                self.y += MOVE_KEYS[key][1]

            case tcod.event.KeySym.f:
                print("found an f")
                target = self.engine.map.get_blocking_entity_at_location(self.x, self.y)
                if not target:
                    # handle this differently later when things like AoEs are implemented
                    self.engine.add_message("There's nothing to shoot there.")
                    return
                if not self.weapon.can_fire:
                    self.engine.add_message("Your weapon is empty.")
                    return
                action = PlayerFireAction(self.player, target, self.weapon)
                self.engine.switch_handler(HandlerType.GAME)
                return action

            case key if key in ESCAPE_KEYS:
                self.engine.switch_handler(HandlerType.GAME)