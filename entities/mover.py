from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from render_order import RenderOrder

from .base_entity import BaseEntity
from .modifiers import ModifierProperty

from math import floor

if TYPE_CHECKING:
    from entities.ai.basic_ai import BasicAI

# Mover - an entity that can move
class Mover(BaseEntity):
    def __init__(self, move_speed: int = 10, ai: Optional[BasicAI] = None, **kwargs):
        super().__init__(**kwargs)
        # delay is a measure of how many auts until something can act again
        # when a creature's delay is 0 or less, it acts
        self.delay = 10
        # an entity is "awake" if it needs to act - this will cut down on some
        # of the checks that have to be made later
        self.awake = False
        self._move_speed = move_speed
        self.render_order = RenderOrder.COMBATANT
        if ai != None:
            self.ai = ai(self)

    @property
    def is_alive(self) -> bool:
        return False
    
    @property
    def move_speed(self) -> int:
        modified_value = sum(m.amount for m in self.modifiers if m.property_type == ModifierProperty.MOVEMENT_SPEED and m.multiplicative == False)
        speed = self._move_speed + int(modified_value)
        if self.has_modifier_of_type(ModifierProperty.PLAYER_CRIPPLED):
            speed = floor(speed * 2)
        return speed

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy