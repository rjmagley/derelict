from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from . import MOVE_KEYS, CONFIRM_KEYS, ESCAPE_KEYS

import tcod

from actions.actions import PlayerCastPowerAction
from actions import ActionResult

from powers import PowerTags

if TYPE_CHECKING:
    from game_engine import GameEngine
    from items.ranged_weapon import RangedWeapon
    from powers.base_power import BasePower
    
from .look_event_handler import LookEventHandler
from input_handlers.handler_types import HandlerType

# a lot of this is making assumptions about how power targeting works, i.e.
# that it's always going to be used to hit an enemy
# this is not the case! right now I'm going to handle those cases with some
# conditionals or matches, but it may be wise in the future to have completely
# different targeters/handlers
class PowerTargetingEventHandler(LookEventHandler):

    def __init__(self, engine: GameEngine, power: BasePower):
        super().__init__(engine)
        self.player = self.engine.player
        self.targets = self.engine.map.living_entities_by_distance()
        self.target_index = 0
        self.x = self.targets[self.target_index].x if self.targets else self.player.x
        self.y = self.targets[self.target_index].y if self.targets else self.player.y
        self.handler_type = HandlerType.POWER_TARGETING
        self.power = power
        self.radius = power.radius if hasattr(power, 'radius') else 1
        

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionResult]:
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
                match self.power.tags:

                    #whuh-oh, this can target through transparent walls!
                    case _ if PowerTags.ENEMY_TARGET in self.power.tags:
                        target = self.engine.map.get_blocking_entity_at_location(self.x, self.y)
                        if not target:
                            # handle this differently later when things like AoEs are implemented
                            return ActionResult(False, "There's nothing to target there.")
                        action = PlayerCastPowerAction(self.player, self.power, target).perform()
                        self.engine.switch_handler(HandlerType.GAME)
                        return action
                    
                    case _ if PowerTags.FREE_TARGET in self.power.tags:
                        # at some point adding some functions like "isPositionVisible"
                        # to the FloorMap class might be wise
                        if not self.engine.map.visible[self.x, self.y]:
                            return ActionResult(False, "You can't see that location.")
                        action = PlayerCastPowerAction(self.player, self.power, x = self.x, y = self.y).perform()
                        self.engine.switch_handler(HandlerType.GAME)
                        return action


            case key if key in ESCAPE_KEYS:
                self.engine.switch_handler(HandlerType.GAME)
                return ActionResult(False)