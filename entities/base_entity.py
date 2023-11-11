from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Optional

if TYPE_CHECKING:
    from floor_map import FloorMap
    from game_engine import GameEngine

import math

import color

from render_order import RenderOrder

# BaseEntity - the most basic entity class
# basically, anything that isn't a map tile - players, enemies, items, etc.
class BaseEntity():

    engine: GameEngine

    # char can be a single character, or a Unicode code point
    # https://python-tcod.readthedocs.io/en/latest/tcod/charmap-reference.html#code-page-437 for reference
    def __init__(self, map = None, x: int | None = None, y: int | None = None, char: str=chr(0x2022), color: Tuple[int, int, int] = color.white, name: str="<unnamed>", blocks_movement: bool=False, render_order: RenderOrder = RenderOrder.CORPSE):
        
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        if map:
            self.map = map
            map.entities.add(self)
            self.engine = map.engine
            self.x = x
            self.y = y
        self.move_speed = 0

    def distance(self, target: BaseEntity):
        return math.sqrt(
            (target.x - self.x) ** 2 +
            (target.y - self.y) ** 2
        )

    # sets map and other appropriate data
    # used in situations where an item may want to be generated without being
    # placed on the map yet
    def set_map(self, map, x: int, y: int) -> None:
        self.map = map
        map.entities.add(self)
        self.engine = map.engine
        self.x = x
        self.y = y

    def move(self, x, y):
        raise NotImplementedError