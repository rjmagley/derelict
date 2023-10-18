from __future__ import annotations

from typing import List, Tuple

import tcod
import numpy
from random import randint

from entities.mover import Mover
from actions.actions import MeleeAction, MovementAction, WaitAction, PlayerFireAction

class BasicAI():
    
    entity: Mover

    def __init__(self, entity: Mover):
        self.entity = entity
        self.path: List[Tuple[int, int]] = []

    def get_path_to(self, x: int, y: int) -> List[Tuple[int, int]]:

        cost = numpy.array(self.entity.map.tiles['walkable'], dtype=numpy.int8)

        for e in self.entity.map.entities:
            if e.blocks_movement and cost[e.x, e.y]:
                cost[e.x, e.y] += 10

        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y))

        path: List[List[int]] = pathfinder.path_to((x, y))[1:].tolist()

        return [(index[0], index[1]) for index in path]

    def perform(self) -> None:
        pass


# BasicHostile - a hostile AI that wants to close to melee range and attack
class BasicHostile(BasicAI):

    def __init__(self, entity: Enemy):
        super().__init__(entity)
        self.entity = entity
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> ActionResult:
        
        target = self.entity.engine.player
        # print(f"{self.entity.name} performing action")
        destination_x = target.x - self.entity.x
        destination_y = target.y - self.entity.y
        distance = max(abs(destination_x), abs(destination_y))

        # enemies need to pursue players even if the player isn't visible
        # ideally going to the last known location rather than just innately
        # knowing where they are
        if self.entity.map.visible[self.entity.x, self.entity.y]:
            # print(f"{self.entity.name} has a visible target")
            print(f"distance to target: {distance}")
            if distance == 1 and randint(1,10) > 5:
                print("performing melee")
                return MeleeAction(self.entity, target).perform()
            if distance <= 10 and randint(1,10) > 5:
                # print(f"{self.entity.name} attacking target")
                return PlayerFireAction(self.entity, target, self.entity.ranged_weapons[0]).perform()

            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            destination_x, destination_y = self.path.pop(0)
            return MovementAction(self.entity,
                destination_x - self.entity.x,
                destination_y - self.entity.y).perform()

        return WaitAction(self.entity).perform()

