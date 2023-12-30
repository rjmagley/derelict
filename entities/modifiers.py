from enum import auto, StrEnum
from decimal import Decimal
from dataclasses import dataclass

class ModifierProperty(StrEnum):
    MOVEMENT_SPEED = "movement speed"

@dataclass
class Modifier:
    property_type: ModifierProperty
    amount: int | Decimal
    # how long the modifier lasts - for most modifiers this will be in auts,
    # some may be based on number of attacks the player makes, etc.
    duration: int

    
    multiplicative: bool
    # the below are for displaying in the UI, for the player status
    # short-name should be five chars
    short_name: str
    fg_color: tuple[int, int, int]
    bg_color: tuple[int, int, int]

    # by default modifiers tick down with every aut, per the above duration
    # nothing is behaving otherwise Yet but it seems useful to pay attention to
    is_timed: bool = True
