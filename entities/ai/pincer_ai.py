from __future__ import annotations

from typing import TYPE_CHECKING

import tcod
import numpy
from random import randint

import color

from .basic_ai import BasicHostile

import random

from actions.actions import MeleeAction, MovementAction, WaitAction, PlayerFireAction

if TYPE_CHECKING:
    from entities.mover import Mover

# PincerAI - wants to surround the player in a pincer with other enemies
# we do this by determining at creation if they want to be above or below
# the player, then using that to modify the get_path_to function

# this will probably be more interesting with enemies that can teleport themselves
# around, or enemies that can spawn packs of these, etc.
class PincerAI(BasicHostile):

    def __init__(self, entity: Mover):
        super().__init__(entity)
        # 'heading' is the side of the player this enemy wants to be on
        # 'north' is above, 'south' is below
        if random.random() > .5:
            self.heading = 'north'
        else:
            self.heading = 'south'

    def get_path_to(self, x: int, y: int) -> List[Tuple[int, int]]:

        target = self.entity.engine.player
        cost = numpy.array(self.entity.map.tiles['walkable'], dtype=numpy.int8)

        # increasing the cost based on heading
        if self.heading == 'north':
            cost[target.x:21, 0:160] += 9
        elif self.heading == 'south':
            cost[0:target.x+1, 0:160] += 9


        for e in self.entity.map.entities:
            if e.blocks_movement and cost[e.x, e.y]:
                cost[e.x, e.y] += 100

        cost = numpy.multiply(cost, self.entity.map.tiles['walkable'])

        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y))

        path: List[List[int]] = pathfinder.path_to((x, y))[1:].tolist()

        # test

        return [(index[0], index[1]) for index in path]

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
            print(f"{self.entity.name} has a visible target")
            self.last_visible_x = target.x
            self.last_visible_y = target.y
            print(f"distance to target: {distance}")

            if distance == 1 and randint(1,10) > 5:
                print("performing melee")
                return MeleeAction(self.entity, target).perform()

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
            print(f"attempting to move to {destination_x} {destination_y}")
            return MovementAction(self.entity,
                destination_x - self.entity.x,
                destination_y - self.entity.y).perform()

        return WaitAction(self.entity).perform()