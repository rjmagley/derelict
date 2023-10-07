from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.player import Player

# base class for psychic powers
# for now, only the player has access to these
class BasePower():

    def __init__(self, caster: Player, power_cost: int = 1, name: str = "<unnamed power>"):

        self.caster = caster
        self.power_cost = power_cost
        self.name = name

        self.description = "no description"
        self.radius = None

    @property
    def can_cast(self) -> bool:
        return self.caster.psy_points >= self.power_cost

    def cast(self) -> None:
        raise NotImplementedError
