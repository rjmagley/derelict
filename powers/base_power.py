from __future__ import annotations

from input_handlers.handler_types import HandlerType

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from entities.player import Player
    from . import PowerType

# base class for psychic powers
# for now, only the player has access to these
class BasePower():

    handler_type: Optional[HandlerType]
    power_type: Optional[PowerType]

    def __init__(self, caster: Player):

        self.caster = caster
        self.power_cost = 1
        self.name = "<unnamed power>"
        self.handler_type = None
        self.description = "no description"
        self.radius = 1
        # some powers need a target, some are just cast automatically - buffing
        # the player, hitting all enemies in LOS, etc
        self.is_targeted = True
        self.power_type = None

    # making it easier to access the engine for message generation purposes
    @property
    def engine(self):
        return self.caster.engine

    @property
    def can_cast(self) -> bool:
        return self.caster.psy_points >= self.power_cost

    def cast(self) -> None:
        raise NotImplementedError
