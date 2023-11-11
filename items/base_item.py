from typing import Optional, TYPE_CHECKING, Type

from entities.base_entity import BaseEntity

from render_order import RenderOrder

# BaseItem - the base for all items
# "items" being things that exist in your inventory
# ammunition is a "pickup" - go look at the Pickup class
class BaseItem(BaseEntity):

    def __init__(self, description: Optional[str] = None, **kwargs):
        super().__init__(**kwargs, blocks_movement = False, render_order = RenderOrder.ITEM)
        self.description = "<no description lmao?>"