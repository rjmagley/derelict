from __future__ import annotations

from typing import Tuple

from items import AmmunitionType
from items.base_item import BaseItem
from entities.pickups.ammo_pickup import AmmoPickup

# the Magazine represents the player equipment for managing and
# creating ammunition
# it's split off into a seperate class so that the Player class doesn't get
# unwieldy - there are also potentially some situations where having enemies
# with a limited/regenerating ammunition pool would be neat

class Magazine(BaseItem):

    def __init__(self,
        max_ammo_count: Tuple[int, int, int, int] = (1000, 1000, 1000, 1000), empty: bool = False, **kwargs):
        super().__init__(name = "Basic Magazine", char = "$", **kwargs)
        self.maximum_ammunition = {
            AmmunitionType.LIGHT: max_ammo_count[0],
            AmmunitionType.HEAVY: max_ammo_count[1],
            AmmunitionType.EXPLOSIVE: max_ammo_count[2],
            AmmunitionType.EXOTIC: max_ammo_count[3]
        }

        self.ammunition = {
            AmmunitionType.LIGHT: 0 if empty else max_ammo_count[0],
            AmmunitionType.HEAVY: 0 if empty else max_ammo_count[1],
            AmmunitionType.EXPLOSIVE: 0 if empty else max_ammo_count[2],
            AmmunitionType.EXOTIC: 0 if empty else max_ammo_count[3]
        }

    def get_max_ammo(self, ammo_type: AmmunitionType) -> int:
        return self.maximum_ammunition[ammo_type]

    def get_current_ammo(self, ammo_type: AmmunitionType) -> int:
        return self.ammunition[ammo_type]

    def get_percentage(self, ammo_type: AmmunitionType) -> str:
        return f"{self.ammunition[ammo_type]/self.maximum_ammunition[ammo_type]*100:.0f}"

    # returns false if the requested amount of ammunition cannot be provided
    def spend_ammo(self, ammo_type: AmmunitionType, amount: int) -> bool:
        if amount > self.get_current_ammo(ammo_type):
            return False
        self.ammunition[ammo_type] -= amount
        return True

    # for right now, ammo is just instantly available
    # it might be cool to add a system where whatever you pick up needs to
    # first be "processed" over time
    def add_ammo(self, pickup: AmmoPickup) -> None:
        self.ammunition[pickup.ammo_type] = min(self.ammunition[pickup.ammo_type] + pickup.amount, self.maximum_ammunition[pickup.ammo_type])