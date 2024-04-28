from enum import auto, Enum


class RenderOrder(Enum):
    CORPSE = auto()
    PICKUP = auto()
    ITEM = auto()
    EFFECT = auto()
    COMBATANT = auto()
    