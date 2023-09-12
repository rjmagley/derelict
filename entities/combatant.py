from .base_entity import BaseEntity
from .mover import Mover

# Combatant - an entity that can fight, take damage, etc.
class Combatant(Mover):

    def __init__(self, hp: int=0, **kwargs):
        super().__init__(**kwargs)
        self.hp = hp