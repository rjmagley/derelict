from __future__ import annotations

import random

from typing import TYPE_CHECKING, Optional

from . import ArmorType, ArmorName, ArmorProperty
from .base_armor import BaseArmor

import color

if TYPE_CHECKING:
    from .base_armor import BaseArmor

# this function generates rare armor pieces - they have special properties
# beyond standard armor, in the same way that rare weapons supercede normal
# weapons

# there's a way to get everything from an enum class rather than typing them out
# one by one, I am Sure
rare_armors = [ArmorName.TS_ONE]

def get_rare_armor(specific_armor: Optional[ArmorName] = None) -> BaseArmor:

    if specific_armor:
        armor_choice = specific_armor
    else:
        armor_choice = random.choice(rare_armors)

    match armor_choice:
        # this one I'm going to experiment with insuring armors have one specifc
        # property, and then a secondary random one
        case ArmorName.TS_ONE:
            new_armor = BaseArmor(
                armor_type=ArmorType.HELMET,
                armor_points=6,
                damage_resist=0,
                name="Truesight One Monocular",
                color=color.blue
            )

    return new_armor
