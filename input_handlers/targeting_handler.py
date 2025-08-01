from __future__ import annotations

from typing import TYPE_CHECKING

from . import MOVE_KEYS, WAIT_KEYS, CURSOR_Y_KEYS, CONFIRM_KEYS, ESCAPE_KEYS

import tcod

from actions.actions import PlayerFireAction
from actions import ActionResult

if TYPE_CHECKING:
    from game_engine import GameEngine
    from items.ranged_weapon import RangedWeapon
    
from .look_event_handler import LookEventHandler
from input_handlers.handler_types import HandlerType

class TargetingEventHandler(LookEventHandler):

    x: int
    y: int

    def __init__(self, engine: GameEngine, weapon: RangedWeapon):
        super().__init__(engine)
        self.player = self.engine.player
        # self.targets = self.engine.map.living_entities_by_distance()
        self.targets = sorted(self.engine.map.visible_enemies, key= lambda e: e.distance(self.player))
        self.target_index = 0
        self.x = self.targets[self.target_index].x if self.targets else self.player.x
        self.y = self.targets[self.target_index].y if self.targets else self.player.y
        self.handler_type = HandlerType.TARGETING
        self.weapon = weapon
        self.radius = weapon.radius if hasattr(weapon, 'radius') else 1
        

    def ev_keydown(self, event: tcod.event.KeyDown) -> ActionResult:
        key = event.sym

        match key:
            case key if key in MOVE_KEYS and self.engine.map.in_bounds(self.x + MOVE_KEYS[key][0], self.y + MOVE_KEYS[key][1]):
                self.x += MOVE_KEYS[key][0]
                self.y += MOVE_KEYS[key][1]

            case tcod.event.KeySym.TAB:
                self.target_index = (self.target_index + 1) % len(self.targets)
                self.x = self.targets[self.target_index].x if self.targets else self.player.x
                self.y = self.targets[self.target_index].y if self.targets else self.player.y

            case tcod.event.KeySym.f:
                target = self.engine.map.get_blocking_entity_at_location(self.x, self.y)
                # for now, there's no blind-shooting
                if not self.engine.map.visible[self.x, self.y]:
                    return ActionResult(False, "You can't see there.")
                if not target:
                    # handle this differently later when things like AoEs are implemented
                    return ActionResult(False, "There's nothing to shoot there.")
                if not self.weapon.can_fire:
                    return ActionResult(False, "Your weapon is empty.")
                if not self.engine.map.is_los_clear(target, self.player):
                    return ActionResult(False, "There's not a clear shot to the target.")
                action = PlayerFireAction(self.player, target, self.weapon).perform()
                self.engine.switch_handler(HandlerType.GAME)
                return action

            case key if key in ESCAPE_KEYS:
                self.engine.switch_handler(HandlerType.GAME)
                return ActionResult(False)