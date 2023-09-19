import random
from .melee_weapon import MeleeWeapon

def place_random_weapon(x: int, y: int) -> MeleeWeapon:
    return MeleeWeapon(x=x, y=y, damage_die=4, die_count=2, name="Weapon")