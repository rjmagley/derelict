from enum import auto, StrEnum
from decimal import Decimal
from dataclasses import dataclass

class ModifierProperty(StrEnum):
    MOVEMENT_SPEED = "movement speed"

@dataclass
class Modifier:
    property_type: ModifierProperty
    amount: int
    duration: int
    multiplicative: bool
