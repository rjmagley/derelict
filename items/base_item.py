from typing import Optional, TYPE_CHECKING, Type

from entities.base_entity import BaseEntity

from render_order import RenderOrder

class BaseItem(BaseEntity):

    def __init__(self, description: Optional[str] = None, **kwargs):
        super().__init__(**kwargs, blocks_movement = False, render_order = RenderOrder.ITEM)
        self.description = "<no description lmao?>"