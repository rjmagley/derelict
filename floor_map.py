from __future__ import annotations

from typing import Iterable, TYPE_CHECKING, List

import numpy
import tile_types

from tcod.console import Console

if TYPE_CHECKING:
    from entities.base_entity import BaseEntity
    from game_engine import GameEngine

# FloorMap - contains all the data for a given floor, including its layout
# should also probably contain its entities if we want the player to be able to
# go up and down floors at will
class FloorMap():
    def __init__(self, engine: GameEngine, width: int, height: int, entities: Iterable[BaseEntity] = {}) -> None:
        self.engine = engine
        self.width = width
        self.height = height
        self.entities = entities
        self.tiles = numpy.full((width, height), fill_value=tile_types.wall, order="F")

        self.visible = numpy.full((width, height), fill_value=False, order='F')
        self.explored = numpy.full((width, height), fill_value=False, order='F')


    def get_blocking_entity_at_location(self, x: int, y: int) -> Optional[BaseEntity]:

        for e in self.entities:
            if e.x == x and e.y == y and e.blocks_movement == True:
                return e

        return None

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        console.rgb[0:self.width, 0:self.height] = numpy.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles['light'], self.tiles['dark']],
            default=tile_types.unseen
        )
        for e in (entity for entity in self.entities if self.visible[entity.x, entity.y]):
            console.print(x=e.x, y=e.y, fg=e.color, string=e.char)
