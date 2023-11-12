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

        # testing some stuff
        # for l in cost:
        #     print(str(cost))
        
        # delete this block later
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
        self.last_visible_x = None
        self.last_visible_y = None

    def perform(self) -> ActionResult:
        
        target = self.entity.engine.player
        # print(f"{self.entity.name} performing action")
        destination_x = target.x - self.entity.x
        destination_y = target.y - self.entity.y
        distance = max(abs(destination_x), abs(destination_y))

        # enemies need to pursue players even if the player isn't visible
        # ideally going to the last known location rather than just innately
        # knowing where they are

        # this implementation is not perfect - enemies will chase the player,
        # but if the player is not visible when they reach the player's last
        # known destination, they stop - might want backup options

        # this currently relies on the player being in the enemy's FOV when the 
        # enemy has a turn - enemies don't have their own FOV (yet?)
        if self.entity.map.visible[self.entity.x, self.entity.y]:
            self.last_visible_x = target.x
            self.last_visible_y = target.y


            if distance == 1 and randint(1,10) > 5:
                print("performing melee")
                return MeleeAction(self.entity, target).perform()

            # need to check if entity can actually be targeted

            elif self.entity.map.is_los_clear(self.entity, target):
                if self.entity.ranged_weapons[0].weapon_in_range(self.entity, target) and randint(1,10) > 5 and self.entity.ranged_weapons[0].can_fire:
                    # print(f"{self.entity.name} attacking target")
                    return PlayerFireAction(self.entity, target, self.entity.ranged_weapons[0]).perform()

            self.path = self.get_path_to(target.x, target.y)

        elif self.last_visible_x != None and self.last_visible_y != None:
            print(f"{self.entity.name} has no visible target, pathing to last known")
            if self.last_visible_x == self.entity.x and self.last_visible_y == self.entity.y:
                print("lost player")
                self.last_visible_x = None
                self.last_visible_y = None
                self.path = []
            else:
                self.path = self.get_path_to(self.last_visible_x, self.last_visible_y)

        if len(self.path) > 0:
            destination_x, destination_y = self.path.pop(0)
            return MovementAction(self.entity,
                destination_x - self.entity.x,
                destination_y - self.entity.y).perform()

        return WaitAction(self.entity).perform()

