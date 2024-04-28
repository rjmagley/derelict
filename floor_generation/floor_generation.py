from __future__ import annotations

from typing import Tuple, Iterator, List, TYPE_CHECKING

import numpy

if TYPE_CHECKING:
    from game_engine import GameEngine

import math
import random

import tcod

from floor_map import FloorMap
from entities.player import Player
import tile_types
from entities import monsters
from items.weapon_generator import place_random_common_weapon
from items.rare_armor import get_rare_armor

from .vault_loader import VaultLoader

# Room - generic room class, keeps track of the center of the room
class Room():
    def __init__(self, x: int, y: int, width: int, height: int, tile_data: List[List[str]]):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tiles = numpy.full((width, height), fill_value=tile_types.wall, order="F")
        for y in range(0, height):
            for x in range(0, width):

                # this just parses each charater from the vault data to turn
                # into the appropriate tile entity
                match tile_data[y][x]:
                    case '#':
                        self.tiles[x, y] = tile_types.wall
                    case '.':
                        self.tiles[x, y] = tile_types.floor
                    case 'T':
                        self.tiles[x, y] = tile_types.transparent_wall
                    case 'C':
                        self.tiles[x, y] = tile_types.chasm


    @property
    def center(self) -> Tuple[int, int]:
        return math.floor(self.x + self.width/2), math.floor(self.y + self.height/2)

    def place_to_floor(self, floor: FloorMap) -> None:
        floor.tiles[slice(self.x, self.x + self.width), slice(self.y, self.y+self.height)] = self.tiles


# RectangularRoom - rooms that are a rectangle
# this isn't actually a thing anymore but I do Not want to refactor this now
class RectangularRoom(Room):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# at some point I need to just remove the height parameter - maps are twenty
# units tall, all the time
def generate_floor(width: int, height: int, engine: GameEngine, difficulty: int = 1) -> FloorMap:

    vault_loader = VaultLoader()

    player = engine.player
    floor = FloorMap(engine, width, height, entities={player})

    rooms: List[Room] = []

    # place entry and exit areas
    entry_data = vault_loader.get_entry_vault()
    entry_room = RectangularRoom(x=0, y=0, width=entry_data['width'], height=entry_data['height'], tile_data=entry_data['map'])
    entry_room.place_to_floor(floor)

    
    player.x, player.y = entry_room.center

    rooms.append(entry_room)
    

    x_offset = 10

    while x_offset < width - 10:
        new_data = vault_loader.get_vault()
        while new_data['width'] > width-x_offset:
            new_data = vault_loader.get_vault()
        new_room = RectangularRoom(x=x_offset, y=random.randint(0, 20-new_data['height']), width=new_data['width'], height=new_data['height'], tile_data=new_data['map'])
        rooms.append(new_room)
        new_room.place_to_floor(floor)
        place_enemies(new_room, floor)
        place_items(new_room, floor)
        x_offset += new_room.width

    exit_room = RectangularRoom(x=width-entry_data['width'], y=height-entry_data['height'], width=entry_data['width'], height=entry_data['height'], tile_data=entry_data['map'])

    exit_room.place_to_floor(floor)
    rooms.append(exit_room)

    # placing downstairs

    
    downstairs_location = random.choice([x for x in range(0, 20) if floor.tiles['walkable'][-1, x]])

    floor.downstairs = [width-1, downstairs_location]

    print(floor.downstairs)

    floor.tiles[-1, downstairs_location] = tile_types.down_stairs

    return floor

def place_enemies(room: Room, floor: FloorMap) -> None:
    # this will require a grand refactor in the future - right now, as
    # difficulty increases, the only real change is the number of enemies -
    # eventually this needs to be set up to increase the variety of enemies,
    # with stronger enemies on later floors - as well as things like replacing
    # some enemies with "packs" of lower-level ones, to make things like AOE
    # weapons useful
    number_mobs = random.randint(2+floor.engine.difficulty_level, 5+floor.engine.difficulty_level)
    for i in range(number_mobs):
        x = random.randint(room.x, room.width + room.x - 1)
        y = random.randint(room.y, room.height + room.y - 1)
        if floor.tiles[x, y] == tile_types.floor:
            if not any (e.x == x and e.y == y for e in floor.entities):
                monster_choice = random.randint(1, 10)
                if monster_choice <= 2:
                    # add multiple kobolds
                    # this is super hacky; need a way to spawn multiple enemies
                    # in an area
                    floor.entities.add(monsters.create_kobold(x=x, y=y, map=floor))
                    x = random.randint(room.x, room.width + room.x - 1)
                    y = random.randint(room.y, room.height + room.y - 1)
                    if not any (e.x == x and e.y == y for e in floor.entities):
                        floor.entities.add(monsters.create_kobold(x=x, y=y, map=floor))
                elif monster_choice <= 7:
                    floor.entities.add(monsters.create_goblin(x=x, y=y, map=floor))
                else:
                    floor.entities.add(monsters.create_hobgoblin(x=x, y=y, map=floor))


def place_items(room: Room, map: FloorMap) -> None:
    # this also needs a revamp in the future - as difficulty increases, weapon
    # rarity should increase as well
    x = random.randint(room.x+1, room.x+room.width-2)
    y = random.randint(room.y+1, room.y+room.height-2)
    if map.tiles['walkable'][x, y]:
        map.entities.add(place_random_common_weapon(x, y, map))

    # this is a hacky test to just get some armor in
    # this will be revamped later
    x = random.randint(room.x+1, room.x+room.width-2)
    y = random.randint(room.y+1, room.y+room.height-2)
    if map.tiles['walkable'][x, y]:
        new_armor = get_rare_armor()
        map.place_entity_on_map(new_armor, x, y)


def generate_test_floor(width: int, height: int, engine: GameEngine) -> FloorMap:

    player = engine.player
    player.x, player.y = 5, 5
    floor = FloorMap(engine, width, height, entities={player})

    floor.tiles[1:159, 1:19] = tile_types.floor

    floor.tiles[10:20, 5:15] = tile_types.wall
    floor.tiles[40:50, 10:25] = tile_types.wall
    floor.tiles[70:100, 5:25] = tile_types.wall
    floor.tiles[3:113, 2:4] = tile_types.wall


    floor.entities.add(monsters.create_dummy(x=6, y=6, map=floor))
    floor.entities.add(monsters.create_dummy(x=66, y=6, map=floor))

    return floor

def generate_test_floor2(width: int, height: int, engine: GameEngine) -> FloorMap:


    floor = generate_floor(160, 20, engine)
    # floor.tiles[1:20, 1:19] = tile_types.floor
    # floor.tiles[139:159, 1:19] = tile_types.floor

    return floor