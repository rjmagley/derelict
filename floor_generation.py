from __future__ import annotations

from typing import Tuple, Iterator, List, TYPE_CHECKING

if TYPE_CHECKING:
    from game_engine import GameEngine

import math
import random

import tcod

from floor_map import FloorMap
from entities.player import Player
import tile_types
from entities import monsters

# right now I'm following the tutorial's general implementation of this stuff
# later I'd rather do something vault-based, like DCSS does

# Room - generic room class, keeps track of the center of the room
class Room():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @property
    def center(self) -> Tuple[int, int]:
        return self.x, self.y



# RectangularRoom - rooms that are a rectangle
class RectangularRoom(Room):
    def __init__(self, width: int, height: int, **kwargs):
        super().__init__(**kwargs)
        self.x1 = self.x - math.floor(width/2)
        self.x2 = self.x + math.ceil(width/2)
        self.y1 = self.y - math.floor(height/2)
        self.y2 = self.y + math.ceil(height/2)

    @property
    def inner(self) -> Tuple[slice, slice]:
        # print(slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2))
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other_room: RectangularRoom) -> bool:
        # print(f"self x: {self.x} self y {self.y}")
        # print(f"other x: {other_room.x1} {other_room.x2}")
        # print(f"other y: {other_room.y1} {other_room.y2}")
        return (
            self.x > other_room.x1 and
            self.x < other_room.x2 and
            self.y > other_room.y1 and
            self.y < other_room.y2
        )

def generate_floor(width: int, height: int, engine: GameEngine) -> FloorMap:

    player = engine.player
    floor = FloorMap(engine, width, height, entities={player})

    rooms: List[Room] = []

    for r in range(16):
        new_room_width = random.randint(6, 12)
        new_room_height = random.randint(6, 12)

        x = random.randint(0 + math.floor(new_room_width / 2), width - math.floor(new_room_width / 2) - 1)
        y = random.randint(0 + math.floor(new_room_height / 2), height - math.floor(new_room_height / 2) - 1)

        new_room = RectangularRoom(x=x, y=y, width=new_room_width, height=new_room_height)


        if any(new_room.intersects(n) for n in rooms):
            continue

        floor.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            player.x, player.y = new_room.center
        else:
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                floor.tiles[x, y] = tile_types.floor

        place_enemies(new_room, floor)

        rooms.append(new_room) 


    return floor

def tunnel_between(start: Tuple[int, int], end: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    x1, y1 = start
    x2, y2 = end

    if random.random() < 0.5:
        corner_x, corner_y = x2, y1
    else:
        corner_x, corner_y = x1, y2

    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y

def place_enemies(room: Room, map: FloorMap) -> None:

    # number_mobs = random.randint(0, 3)
    # for i in range(number_mobs):
    #     x = random.randint(room.x1 + 1, room.x2 - 1)
    #     y = random.randint(room.y1 + 1, room.y2 - 1)
    #     print(f"attempting placement at {x, y}")
    #     if not any (e.x == x and e.y == y for e in map.entities):
    #         map.entities.add(monsters.create_goblin(x=x, y=y, map=map))
    #         print(map.entities)
    #     else:
    #         print("placement failed")
    pass