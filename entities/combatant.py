from __future__ import annotations

from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING

from .base_entity import BaseEntity
from .mover import Mover

import color

from render_order import RenderOrder

# from entities.ai.basic_ai import BasicAI

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
        self.render_order = RenderOrder.COMBATANT
        if ai != None:
            self.ai = ai(self)

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.ai:
            self.die()

    @property
    def is_alive(self) -> bool:
        return self.ai != None

    def attack(self, target: Combatant):
        damage = self.power - target.defense
        output_string = f"{self.name} attacks {target.name} "
        if damage > 0:
            output_string += f"for {damage} damage."
        else:
            output_string += "for no damage."
        self.engine.message_log.add_message(output_string)
        target.hp -= damage
        

    def die(self) -> None:
        self.engine.message_log.add_message(f"{self.name} dies!", color.red)
        self.char = "%"
        self.color = color.red
        self.blocks_movement = False
        self.ai = None
        self.name = f"remains of {self.name}"
        self.render_order = RenderOrder.CORPSE