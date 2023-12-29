from enum import auto, StrEnum
from decimal import Decimal
from dataclasses import dataclass

class ModifierProperty(StrEnum):
    MOVEMENT_SPEED = "movement speed"

@dataclass
class Modifier:
    property_type: ModifierProperty
    amount: int | Decimal
    duration: int
    multiplicative: bool
    # the below are for displaying in the UI, for the player status
    # short-name should be five chars
    short_name: str
    fg_color: tuple[int, int, int]
    bg_color: tuple[int, int, int]
