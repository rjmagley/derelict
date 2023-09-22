import random
from .melee_weapon import MeleeWeapon
from .ranged_weapon import RangedWeapon

def place_random_melee_weapon(x: int, y: int) -> MeleeWeapon:
    return MeleeWeapon(x=x, y=y, damage_die=4, die_count=2, name="Weapon")

def place_random_ranged_weapon(x: int, y: int) -> RangedWeapon:
    return RangedWeapon(x=x, y=y, damage_die=4, die_count=2, magazine_size = 10, burst_count = 2, char="{", name="Pistol")