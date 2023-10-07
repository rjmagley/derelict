from __future__ import annotations

from typing import TYPE_CHECKING

from input_handlers.handler_types import HandlerType
from powers.base_power import BasePower

if TYPE_CHECKING:
    from entities.player import Player

# Smite - selects one unit targeted by the player, then some random number
# of other units around that unit, and deals damage to N of them

# the damage is rather low, but if you target one unit all by itself in the
# radius, it can hit that unit multiple times
# won't target player
class Smite(BasePower):
        def __init__(self, **kwargs):

            super().__init__(**kwargs)

            self.power_cost = 2
            self.radius = 3
            # self.handler_type
