from __future__ import annotations

from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING

from .base_entity import BaseEntity
from .mover import Mover

import color

from render_order import RenderOrder

# 

if TYPE_CHECKING:
    from entities.combatant import Combatant
    from floor_map import FloorMap

# Combatant - an entity that can fight, take damage, etc.
# also something that has an AI - should that be split later?
class Combatant(Mover):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def is_alive(self) -> bool:
        return self.ai != None

    # returning a string to pass to the ActionResult
    # will eventually need to also return time taken
    # may need to just return the ActionResult itself
    def ranged_attack(self, target: Combatant) -> str:
        raise NotImplementedError

        
    def melee_attack(self, target: Combatant) -> str:
        raise NotImplementedError

    def die(self) -> None:
        raise NotImplementedError

    def take_damage(self, damage: int) -> None:
        raise NotImplementedError

    def periodic_refresh(self):
        pass