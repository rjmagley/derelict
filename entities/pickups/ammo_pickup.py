from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Optional

from . import BasePickup, PickupType
from items import AmmunitionType

from render_order import RenderOrder
import color

if TYPE_CHECKING:
    from game_engine import GameEngine
    from floor_map import FloorMap

# AmmoPickup - refills the player's ammo
# enemies don't interact with this - their weapons should either recharge
# or have limited ammo
class AmmoPickup(BasePickup):

    engine: GameEngine

    def __init__(self, pickup_type: PickupType, amount: int, description: Optional[str] = None, ** kwargs):
        super().__init__(**kwargs)
        self.description = "<descriptionless lmao?>"
        self.char = "|"
        self.pickup_type = pickup_type
        self.render_order = RenderOrder.PICKUP
        match pickup_type:
            case PickupType.LIGHT_AMMO:
                self.name = "light materiel"
                self.color = color.light_gray
                self.ammo_type = AmmunitionType.LIGHT
            case PickupType.HEAVY_AMMO:
                self.name = "heavy materiel"
                self.color = color.white
                self.ammo_type = AmmunitionType.HEAVY
            case PickupType.EXPLOSIVE_AMMO:
                self.name = "explosive elements"
                self.color = color.yellow
                self.ammo_type = AmmunitionType.EXPLOSIVE
            case PickupType.EXOTIC_AMMO:
                self.name = "exotic elements"
                self.color = color.magenta
                self.ammo_type = AmmunitionType.EXOTIC
        self.amount = amount

    @classmethod
    def generate_pickup(cls, pickup_type, amount):
        return cls(pickup_type, amount)

    def on_consume(self):
        self.engine.map.entities.remove(self)
        del(self)