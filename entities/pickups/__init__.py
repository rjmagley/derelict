from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Optional
from enum import StrEnum

from ..base_entity import BaseEntity

from render_order import RenderOrder

# BasePickup - items that are automatically used upon pickup
# for right now this is primarily ammunition, but may incluse instant-use
# shield capacitors, armor repair, buffs, etc.
class BasePickup(BaseEntity):

    def __init__(self, description: Optional[str] = None, ** kwargs):
        super().__init__(**kwargs, blocks_movement = False, render_order = RenderOrder.ITEM)
        self.description = "<descriptionless lmao?>"

class PickupType(StrEnum):
    LIGHT_AMMO = "light ammunition"
    HEAVY_AMMO = "heavy ammunition"
    EXPLOSIVE_AMMO = "explosive ammunition"
    EXOTIC_AMMO = "exotic ammunition"