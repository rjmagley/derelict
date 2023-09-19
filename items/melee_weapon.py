from .base_weapon import BaseWeapon

class MeleeWeapon(BaseWeapon):

    def __init__(self, **kwargs):
        super().__init__(char='/', **kwargs)