import random

from .base_item import BaseItem

class BaseWeapon(BaseItem):

    def __init__(self, damage_die: int = 1, die_count: int = 1, hands: int = 1, **kwargs):
        super().__init__(**kwargs)
        self.damage_die = damage_die
        self.die_count = die_count
        self.hands = hands

    @property
    def status_string(self) -> str:
        return f"{self.name} - {self.die_count}d{self.damage_die}"

    def roll_damage(self):
        damage = 0
        for i in range(0, self.die_count):
            damage += random.randint(1, self.damage_die)

        return damage