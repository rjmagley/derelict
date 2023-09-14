from __future__ import annotations

from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING

from .base_entity import BaseEntity
from .mover import Mover

from entities.ai.basic_ai import BasicAI

if TYPE_CHECKING:
    from entities.combatant import Combatant
    from floor_map import FloorMap

# Combatant - an entity that can fight, take damage, etc.
# also something that has an AI - should that be split later?
class Combatant(Mover):

    def __init__(self, hp: int, defense: int, power: int, ai: Optional[BasicAI] = None, **kwargs):
        super().__init__(**kwargs)
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.power = power
        if ai != None:
            self.ai = ai(self)

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))

    @property
    def is_alive(self) -> bool:
        return self._hp > 0