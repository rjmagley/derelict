import math
from .enemy import Enemy
from floor_map import FloorMap
from .ai.basic_ai import BasicAI, BasicHostile
import color
from items.ranged_weapon import RangedWeapon

goblin_test_weapons = [
    RangedWeapon(damage_die=3, die_count=2, magazine_size=10, burst_count=2, name='goblin test gun')
]

def create_goblin(x: int, y: int, map: FloorMap) -> Enemy:
    return Enemy(level=1, x=x, y=y, char='g', color=color.green, name='goblin', blocks_movement=True, hp=10, defense=1, ai=BasicHostile, map=map, weapons=goblin_test_weapons)

def create_slow_goblin(x: int, y: int, map: FloorMap) -> Enemy:
    return Enemy(level=1, x=x, y=y, char='g', color=color.yellow, name='goblin', blocks_movement=True, hp=10, defense=2, ai=BasicHostile, map=map, move_speed=15, weapons=goblin_test_weapons)

# def create_orc(x: int, y: int) -> Combatant:
#     return Combatant(x=x, y=y, char='o', color=color.green, name='orc', blocks_movement=True, hp=10, defense=2, power=2, ai=BasicHostile, map=map)

# def create_dummy(x: int, y: int, map: FloorMap) -> Combatant:
#     return Combatant(x=x, y=y, char='o', color=color.yellow, name='dummy', blocks_movement=True, hp=10, defense=20, power=2, ai=BasicAI, map=map)