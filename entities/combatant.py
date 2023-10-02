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


    # @property
    # def hp(self) -> int:
    #     return self._hp

    # @hp.setter
    # def hp(self, value: int) -> None:
    #     self._hp = max(0, min(value, self.max_hp))
    #     if self._hp == 0 and self.ai:
    #         self.die()

    @property
    def is_alive(self) -> bool:
        return self.ai != None

    # returning a string to pass to the ActionResult
    # will eventually need to also return time taken
    # may need to just return the ActionResult itself
    def ranged_attack(self, target: Combatant) -> str:
        raise NotImplementedError
        # print("attempting attack")
        # damage = self.power
        # print(f"{self.name} attacking {target.name} - damage is {damage}")
        
        # output_string = f"{self.name} attacks {target.name} "
        # if damage > 0:
        #     output_string += f"for {damage} damage."
        # else:
        #     output_string += "for no damage."
        # self.engine.message_log.add_message(output_string)
        # target.take_damage(damage)
        
    def melee_attack(self, target: Combatant) -> str:
        raise NotImplementedError

    def die(self) -> None:
        raise NotImplementedError

    # def die(self) -> None:
    #     self.engine.message_log.add_message(f"{self.name} dies!", color.red)
    #     self.char = "%"
    #     self.color = color.red
    #     self.blocks_movement = False
    #     self.ai = None
    #     self.name = f"remains of {self.name}"
    #     self.render_order = RenderOrder.CORPSE

    # def take_damage(self, damage: int) -> None:
    #     self.hp -= max(0, damage - self.defense)

    def take_damage(self, damage: int) -> None:
        raise NotImplementedError

    def periodic_refresh(self):
        pass