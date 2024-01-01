from __future__ import annotations

from typing import TYPE_CHECKING

from input_handlers.handler_types import HandlerType
from powers.base_power import BasePower
import die_rollers
import color
import random
from . import PowerSkill, PowerTags

from entities.effect_entity import EffectEntity

# Fog - creates a bank of temporary obscuring clouds to block vision
# this is symmetrical - it blocks the player from seeing enemies, too!
# meant to be used to reposition, reload, etc. so that the player doesn't
# take a bunch of damage unexpectedly
# player can cast it on a single enemy to temporarily block them, or on/near
# themselves

class FogPower(BasePower):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.name = "Fog"
        self.power_cost = 1
        self.radius = 3
        self.handler_type = HandlerType.POWER_TARGETING
        self.power_type = PowerSkill.DEFENSE
        self.tags = {PowerTags.FREE_TARGET}

    def cast(self, x: int, y: int, **kwargs):
        current_map = self.caster.engine.map
        # figure out which tiles can be fogged
        potential_tiles = []
        print(f"center is {x}, {y}")
        for i in range(x - self.radius + 1, x + self.radius):
            for j in range(y - self.radius + 1, y + self.radius):
                print(i, j)
                if not current_map.tiles['blocking'][i, j]:
                    potential_tiles.append([i, j])

        fogged_tiles = random.sample(potential_tiles, 5)
        # we always want at least one fog tile where the player fires this power
        fogged_tiles.append([x, y])

        
        for t in fogged_tiles:
            print(t)
            EffectEntity(blocks_vision = True, duration = 200, map = current_map, char = "*", color = color.bright_magenta, x = t[0], y = t[1])