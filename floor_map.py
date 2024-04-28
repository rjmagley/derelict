from __future__ import annotations

from typing import Iterable, TYPE_CHECKING, List, Set, Generator, Optional, Tuple

import numpy
import tile_types

from tcod.console import Console
from tcod.los import bresenham

from entities.combatant import Combatant
from entities.mover import Mover
from entities.enemy import Enemy
from items.base_item import BaseItem
from entities.pickups import BasePickup

from random import choice

if TYPE_CHECKING:
    from entities.base_entity import BaseEntity
    from game_engine import GameEngine
    

# FloorMap - contains all the data for a given floor, including its layout

class FloorMap():
    def __init__(self, engine: GameEngine, width: int, height: int, entities: List[BaseEntity] = []) -> None:
        self.engine = engine
        self.width = width
        self.height = height
        # at some point I'd like to refactor this so that there is not just one
        # list, but several - movers, pickups, items and corpses
        # maybe even projectiles? if I ever want to implement like, slow moving
        # or dodgable projectiles, like crawl's OODs
        self.entities = entities
        # this is part of the refactor listed above - gonna have a seperate layer for "effect" entities
        self.effects = []

        self.downstairs = [0, 0]
        self.tiles = numpy.full((width, height), fill_value=tile_types.wall, order="F")

        self.temporary_los_obstruction = numpy.full((width, height), fill_value = 0, order="F")


        self.visible = numpy.full((width, height), fill_value=False, order='F')
        self.explored = numpy.full((width, height), fill_value=False, order='F')
        # self.map_console = Console(width, height, order="F")

    # a lot of things in here need to be heavily refactored - many of these
    # functions could be compressed into one that accepts some arguments

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

    @property
    def visible_enemies(self) -> List[Enemy]:
        enemies = [e for e in self.entities if isinstance(e, Enemy) and e.is_alive and self.visible[e.x, e.y]]
        return enemies

    # returns True if space is occupied and False otherwise
    def entity_matching_type_at_location(self, entity: BaseEntity, x: int, y: int) -> bool:
        entities = [e for e in self.entities if isinstance(e, type(entity))]
        for e in entities:
            if e.x == x and e.y == y:
                return True

        return False

    def entities_matching_type(self, entity: BaseEntity) -> List[BaseEntity]:
        movers = [e for e in self.entities if isinstance(e, type(entity))]
        return movers

    # a bunch of functions from here down need to be refactored into forms
    # that look for all entities matching a specific type
    # even better once things are refactored so that movers/pickups/items/etc.
    # have their own lists stored in the map information
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

    def get_item_at_location(self, x: int, y: int) -> Optional[BaseItem | BasePickup]:
        for e in [e for e in self.entities if (isinstance(e, BaseItem) or isinstance(e, BasePickup))]:
            if e.x == x and e.y == y:
                return e

        return None

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height



    def living_entities_by_distance(self) -> List[Combatant]:
        entities = [e for e in self.entities if isinstance(e, Combatant) and e.is_alive and e != self.engine.player and self.visible[e.x, e.y]]
        results = sorted(entities, key=lambda e: e.distance(self.engine.player))

        return results

    # tries to place entity on map - if an entity cannot be placed at the given
    # location, tries to place it elsewhere on the map nearby
    # this actually calls one of two functions to handle placement of items and
    # enemies or other entities
    # I might re-rig this for corpse placement too - currently enemies can die
    # and their corpse gets dropped, which may be on top of another corpse,
    # which may cause problems if corpses ever become anything other than
    # decorative... (doom arch-vile noises in distance)
    def place_entity_on_map(self, entity: BaseEntity, x: int, y: int) -> None:
        result = self.get_valid_position_for_entity(entity, x, y)
        if result == None:
            # failed to place entity - silently, for now
            pass

        else:
            entity.set_map(self, *result)
                

    # used to assist placing entities - checks map for entities of a given type
    # at that position and returns that position if valid
    # otherwise iterates in widening radiuses around the position
    def get_valid_position_for_entity(self, entity: BaseEntity, x: int,
        y: int) -> Optional[Tuple[int, int]]:

        # first see if the given position is clear
        # if it is, no more work to do:
        if not self.entity_matching_type_at_location(entity, x, y):
            return x, y

        else:
            # horrible code incoming
            # this will absolutely need refactoring later, the good solution
            # just isn't coming to me - this is absolutely repetitive
            other_entities = self.entities_matching_type(entity)
            loop_iterations = 1

            potential_locations = []
            while True:

                # yes this is repetitive, it re-scans a lot of areas on the map
                # there's probably something interesting to be done with those
                # ranges to skip the repeated sections
                try:
                    for x_position in [x for x in range(x-loop_iterations, x+loop_iterations+1)]:
                        for y_position in [y for y in range(y-loop_iterations, y+loop_iterations+1)]:
                            if self.tiles['walkable'][x_position, y_position] and not self.entity_matching_type_at_location(entity, x_position, y_position):
                                potential_locations.append((x_position, y_position))
                # catch this if we start going out of bounds, ending the loop
                except:
                    return None

                if len(potential_locations) > 0:
                    return choice(potential_locations)
    # returns True if there is a clear path from entity A to entity B - no
    # map-based obstructions in the way
    # this doesn't check to see if another entity is in the path!
    def is_los_clear(self, entity_a: BaseEntity, entity_b: BaseEntity) -> bool:
        points = bresenham((entity_a.x, entity_a.y), (entity_b.x, entity_b.y)).tolist()

        for p in points:
            if self.tiles['blocking'][p[0], p[1]]:
                return False

        return True
    
    def update_temporary_los(self):
        self.temporary_los_obstruction = numpy.full((self.width, self.height), fill_value = 0, order="F")
        for e in [e for e in self.effects if e.blocks_vision == True]:
            self.temporary_los_obstruction[e.x, e.y] = 1
