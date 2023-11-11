from enum import auto, Enum


class RenderOrder(Enum):
    EFFECT = auto()
    CORPSE = auto()
    ITEM = auto()
    PICKUP = auto()
    COMBATANT = auto()