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

    # currently this can stack - maybe it shouldn't?
    # making it not stack would require keeping track of the source of 
    # modifiers, because there are situations where one property can be
    # changed by multiple sources for better or worse - player buffs their speed,
    # uses another power that also causes an incidental speed buff, and is
    # affected by an enemy's speed debuff
    def cast(self):
        self.caster.psy_points -= self.power_cost
        # the 20 below is a magic number - when the player has psy-related 
        # skills, it might be cool to do 20 + some number based on that
        # skill modifier
        self.caster.modifiers.append(
            Modifier(ModifierProperty.MOVEMENT_SPEED, -5, 20, False, " Ala ", color.bright_yellow, color.blue)
        )
        
        self.engine.add_message("Your movement speed increases!", color.bright_yellow)