from .combatant import Combatant
import color

def create_goblin(x: int, y: int) -> Combatant:
    return Combatant(x=x, y=y, char='g', color=color.green, name='goblin', blocks_movement=True, hp=10)

def create_orc(x: int, y: int) -> Combatant:
    return Combatant(x=x, y=y, char='o', color=color.green, name='orc', blocks_movement=True, hp=10)