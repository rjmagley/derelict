from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Optional

from entities.base_entity import BaseEntity

import random

if TYPE_CHECKING:
    from floor_map import FloorMap
    from game_engine import GameEngine
    from modifiers import Modifier, ModifierProperty

import math

import color

from render_order import RenderOrder

# EffectEntity - an entity that represents an environmental effect - smoke, fog, temporary walls, etc.

class EffectEntity(BaseEntity):

    def __init__(self, blocks_vision: bool=True, duration: int=0, **kwargs):

        super().__init__(**kwargs)
        self.blocks_vision = blocks_vision
        self.duration = duration
        self.map.effects.append(self)

        if blocks_vision:
            self.map.temporary_los_obstruction[self.x, self.y] += 1

    def periodic_refresh(self):
        self.duration -= random.randint(1, 3)
        if self.duration <= 0:
            self.map.effects.remove(self)
            self.map.entities.remove(self)
            self.map.temporary_los_obstruction[self.x, self.y] -= 1
