from .base_weapon import BaseWeapon
from . import WeaponType

import random

class MeleeWeapon(BaseWeapon):

    def __init__(self, **kwargs):
        super().__init__(char='/', **kwargs)
        self.owner = None

def place_random_melee_weapon(x: int, y: int, map = None) -> MeleeWeapon:
    weapon_choices = [
        {'die_count': 3, 'damage_die': 5, 'weapon_types': [WeaponType.SWORD], 'name': 'Test Sword', 'hands': 1}
    ]

    weapon_stats = random.choice(weapon_choices)

    return MeleeWeapon(x=x, y=y, map=map, **weapon_stats)
