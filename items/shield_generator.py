from __future__ import annotations

from typing import Tuple
from decimal import Decimal

from items.base_item import BaseItem

# the ShieldGenerator is responsible for the player's shields
# it manages the state of the shield, which the Player can access when
# necessary

# reboot_time is in decauts - the player's refresh function is called every
# 10 auts - the default reboot_time of 10 means the shield regenerates in 100 auts

class ShieldGenerator(BaseItem):

    def __init__(self, max_shield: int = 10, recharge_rate: Decimal = Decimal(1.0), reboot_time: int = 10, **kwargs):
        super().__init__(name = "Basic Shield", char = "]", **kwargs)
        self.max_shield = max_shield
        self.current_shield = max_shield
        self.partial_shield = 0
        self.recharge_rate = recharge_rate
        self.reboot_time = reboot_time
        self.time_to_reboot = 0

    # returns remaining damage to be taken by armor/HP
    def take_damage(self, value: int) -> int:
        if value >= self.current_shield:
            remaining_damage = value - self.current_shield
            self.current_shield = 0
            self.time_to_reboot = self.reboot_time
            return remaining_damage
        else:
            self.current_shield -= value
            return 0

    def regeneration(self) -> None:
        print(f"current time to reboot: {self.time_to_reboot}")
        if self.time_to_reboot == 0:
            if self.current_shield < self.max_shield:
                self.partial_shield += self.recharge_rate
                if self.partial_shield >= 100:
                    self.partial_shield -= 100
                    self.current_shield += 1
        else:
            self.time_to_reboot -= 1
            if self.time_to_reboot == 0:
                self.current_shield = self.max_shield // 3

    def get_shield_status(self) -> str:
        return f"{self.current_shield}/{self.max_shield}"