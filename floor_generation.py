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
from items.ranged_weapon import place_random_ranged_weapon

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

        if len(rooms) > 0:
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                floor.tiles[x, y] = tile_types.floor

        place_enemies(new_room, floor)
        place_items(new_room, floor)

        rooms.append(new_room) 

    # just in case something tries to break out of the walls of the level:
    floor.tiles[0:160, 0:1] = tile_types.wall
    floor.tiles[0:160, 23:24] = tile_types.wall
    floor.tiles[0:1, 0:24] = tile_types.wall
    floor.tiles[159:160, 0:24] = tile_types.wall

    player.x, player.y = 3, 10

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

    number_mobs = random.randint(0, 5)
    for i in range(number_mobs):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)
        print(f"attempting placement at {x, y}")
        if not any (e.x == x and e.y == y for e in map.entities):
            if random.random() > .5: 
                map.entities.add(monsters.create_goblin(x=x, y=y, map=map))
            else:
                map.entities.add(monsters.create_slow_goblin(x=x, y=y, map=map))


def place_items(room: Room, map: FloorMap) -> None:

    x = random.randint(room.x1 + 1, room.x2 - 1)
    y = random.randint(room.y1 + 1, room.y2 - 1)
    map.entities.add(place_random_ranged_weapon(x, y))

def generate_test_floor(width: int, height: int, engine: GameEngine) -> FloorMap:

    player = engine.player
    player.x, player.y = 5, 5
    floor = FloorMap(engine, width, height, entities={player})

    floor.tiles[1:159, 1:19] = tile_types.floor

    floor.tiles[10:20, 5:15] = tile_types.wall
    floor.tiles[40:50, 10:25] = tile_types.wall
    floor.tiles[70:100, 5:25] = tile_types.wall
    floor.tiles[3:113, 2:4] = tile_types.wall

    print(floor)

    floor.entities.add(monsters.create_dummy(x=6, y=6, map=floor))
    floor.entities.add(monsters.create_dummy(x=66, y=6, map=floor))

    return floor

def generate_test_floor2(width: int, height: int, engine: GameEngine) -> FloorMap:

    floor = generate_floor(160, 20, engine)
    floor.tiles[1:20, 1:19] = tile_types.floor
    floor.tiles[139:159, 1:19] = tile_types.floor

    return floor