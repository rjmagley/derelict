import math
from .enemy import Enemy
from floor_map import FloorMap
from .ai.basic_ai import BasicAI, BasicHostile
from .ai.pincer_ai import PincerAI
import color
from items.ranged_recharge_weapon import RangedRechargeWeapon
from items.melee_weapon import MeleeWeapon
from .pickups import PickupType

# having each monster defined in its own file might be a good idea
# or at least having groups of monsters - early vs. late game?
# sorted by type? location? when different locations are added?

goblin_test_weapons = [
    RangedRechargeWeapon(damage_die=5, die_count=2, charge_needed=100, max_charge=100, recharge_rate=1, burst_count=2, minimum_range=7, maximum_range=7, range_interval=7, name='goblin test gun'),
    MeleeWeapon(damage_die=3, die_count=4, name='goblin test fist')
]

hobgoblin_test_weapons = [
    RangedRechargeWeapon(damage_die=6, die_count=3, charge_needed=150, max_charge=150, recharge_rate=1, burst_count=2, minimum_range=8, maximum_range=12, range_interval=7, name='hobgoblintest gun'),
    MeleeWeapon(damage_die=3, die_count=4, name='goblin test fist')
]

kobold_weapons = [
    MeleeWeapon(damage_die=3, die_count=3, name='kobold claws')
]

test_pickups = [None, None, None, (PickupType.LIGHT_AMMO, 10), (PickupType.LIGHT_AMMO, 5), (PickupType.HEAVY_AMMO, 5)]

def create_goblin(x: int, y: int, map: FloorMap) -> Enemy:
    return Enemy(level=1, x=x, y=y, char='g', color=color.green, name='goblin', blocks_movement=True, hp=10, defense=1, ai=BasicHostile, map=map, weapons=goblin_test_weapons, pickup_table=test_pickups)

def create_hobgoblin(x: int, y: int, map: FloorMap) -> Enemy:
    return Enemy(level=1, x=x, y=y, char='g', color=color.yellow, name='hobgoblin', blocks_movement=True, hp=20, defense=2, ai=BasicHostile, map=map, move_speed=15, weapons=goblin_test_weapons,pickup_table=test_pickups)

def create_kobold(x: int, y: int, map: FloorMap) -> Enemy:
    return Enemy(level=1, x=x, y=y, char='k', color=color.yellow, name='kobold', blocks_movement=True, hp=7, defense=0, ai=PincerAI, map=map, move_speed=8, weapons=goblin_test_weapons, pickup_table=test_pickups)

# def create_orc(x: int, y: int) -> Combatant:
#     return Combatant(x=x, y=y, char='o', color=color.green, name='orc', blocks_movement=True, hp=10, defense=2, power=2, ai=BasicHostile, map=map)

# def create_dummy(x: int, y: int, map: FloorMap) -> Combatant:
#     return Combatant(x=x, y=y, char='o', color=color.yellow, name='dummy', blocks_movement=True, hp=10, defense=20, power=2, ai=BasicAI, map=map)