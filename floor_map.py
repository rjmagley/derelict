from __future__ import annotations

from typing import Iterable, TYPE_CHECKING, List, Set, Generator, Optional

import numpy
import tile_types

from tcod.console import Console

from entities.combatant import Combatant
from entities.mover import Mover
from items.base_item import BaseItem

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
        self.downstairs = [0, 0]
        self.tiles = numpy.full((width, height), fill_value=tile_types.wall, order="F")

        self.visible = numpy.full((width, height), fill_value=False, order='F')
        self.explored = numpy.full((width, height), fill_value=False, order='F')
        # self.map_console = Console(width, height, order="F")

    @property
    def living_entities(self) -> Generator[BaseEntity]:
        yield from (e for e in self.entities if isinstance(e, Combatant) and e.is_alive)

    @property
    def awake_entities(self) -> List[Mover]:
        movers = [e for e in self.entities if isinstance(e, Mover) and e.awake == True and e.is_alive]
        return movers

    @property
    def asleep_entities(self) -> List[Mover]:
        movers = [e for e in self.entities if isinstance(e, Mover) and e.awake == False and e.is_alive]
        return movers

    def get_entities_at_location(self, x: int, y: int) -> List[BaseEntity]:
        
        results = []
        
        for e in self.entities:
            if e.x == x and e.y == y:
                results.append(e)

        return sorted(results, key = lambda x: x.render_order.value)

    def get_living_entities_in_radius(self, x: int, y: int, radius: int) -> List[BaseEntity]:
        
        results = []
        
        for e in self.living_entities:
            if e.x in range(x - radius + 1, x + radius) and e.y in range(y - radius + 1, y + radius):
                results.append(e)

        return sorted(results, key = lambda x: x.render_order.value)

    def get_blocking_entity_at_location(self, x: int, y: int) -> Optional[BaseEntity]:

        for e in self.entities:
            if e.x == x and e.y == y and e.blocks_movement == True:
                return e

        return None

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_items_at_location(self, x: int, y: int) -> List[BaseItem]:
        results = []
        for e in [e for e in self.entities if isinstance(e, BaseItem)]:
            if e.x == x and e.y == y:
                results.append(e)

        return results

    def living_entities_by_distance(self) -> List[Combatant]:
        entities = [e for e in self.entities if isinstance(e, Combatant) and e.is_alive and e != self.engine.player and self.visible[e.x, e.y]]
        results = sorted(entities, key=lambda e:  e.distance(self.engine.player))

        return results