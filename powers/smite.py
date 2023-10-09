from __future__ import annotations

from typing import TYPE_CHECKING

from input_handlers.handler_types import HandlerType
from powers.base_power import BasePower
import die_rollers
import color
import random

if TYPE_CHECKING:
    from entities.player import Player
    from entities.enemy import Enemy

# Smite - selects one unit targeted by the player, then some random number
# of other units around that unit, and deals damage to N of them

# the damage is rather low, but if you target one unit all by itself in the
# radius, it can hit that unit multiple times
# won't target player
class Smite(BasePower):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.name = "Smite"
        self.power_cost = 2
        self.radius = 3
        self.handler_type = HandlerType.POWER_TARGETING

    def cast(self, target: Enemy):
        targets = target.map.get_living_entities_in_radius(target.x, target.y, self.radius)
        print(targets)
        for i in range(0, 3):
            target = random.choice(targets)
            damage = die_rollers.roll_dice(3, 4)
            target.take_damage(damage)
            target.engine.add_message(f"The {target.name} takes {damage} damage!", color.cyan)