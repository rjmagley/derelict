from __future__ import annotations

from input_handlers.handler_types import HandlerType

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.player import Player

# base class for psychic powers
# for now, only the player has access to these
class BasePower():

    def __init__(self, caster: Player):

        self.caster = caster
        self.power_cost = 1
        self.name = "<unnamed power>"
        self.handler_type = HandlerType.POWER_TARGETING
        self.description = "no description"
        self.radius = 1

    @property
    def can_cast(self) -> bool:
        return self.caster.psy_points >= self.power_cost

    def cast(self) -> None:
        raise NotImplementedError
