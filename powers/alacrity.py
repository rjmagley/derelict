from __future__ import annotations

from typing import TYPE_CHECKING

from powers.base_power import BasePower
import color
from entities.modifiers import Modifier, ModifierProperty

if TYPE_CHECKING:
    from entities.player import Player

# Alacrity - provides the player a brief boost in movement speed, useful for
# closing gaps or escaping
    
class AlacrityPower(BasePower):

    # you know in retrospect I'm not sure why this power, nor Smite, need kwargs
    # they need to know the caster (i.e. the player, for now)
    # I think I'm leaving it this way for now because at some point we may want
    # to use a similar structure for enemies?
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.name = "Alacrity"
        self.power_cost = 2
        self.handler_type = None
        self.is_targeted = False

    # currently this can stack - maybe it shouldn't
    def cast(self):
        self.caster.psy_points -= self.power_cost
        self.caster.modifiers.append(
            Modifier(ModifierProperty.MOVEMENT_SPEED, -5, 20, False, " Ala ", color.bright_yellow, color.blue)
        )
        
        self.engine.add_message("Your movement speed increases!", color.bright_yellow)