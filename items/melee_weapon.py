from .base_weapon import BaseWeapon


class MeleeWeapon(BaseWeapon):

    def __init__(self, **kwargs):
        super().__init__(char='/', **kwargs)

def place_random_melee_weapon(x: int, y: int) -> MeleeWeapon:
    return MeleeWeapon(x=x, y=y, damage_die=4, die_count=2, name="Weapon")
