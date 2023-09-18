from .combatant import Combatant
from floor_map import FloorMap
from .ai.basic_ai import BasicAI, BasicHostile
import color

def create_goblin(x: int, y: int, map: FloorMap) -> Combatant:
    return Combatant(x=x, y=y, char='g', color=color.green, name='goblin', blocks_movement=True, hp=10, defense=1, power=0, ai=BasicHostile, map=map)

def create_orc(x: int, y: int) -> Combatant:
    return Combatant(x=x, y=y, char='o', color=color.green, name='orc', blocks_movement=True, hp=10, defense=2, power=2, ai=BasicHostile, map=map)

def create_dummy(x: int, y: int, map: FloorMap) -> Combatant:
    return Combatant(x=x, y=y, char='o', color=color.yellow, name='dummy', blocks_movement=True, hp=10, defense=20, power=2, ai=BasicAI, map=map)