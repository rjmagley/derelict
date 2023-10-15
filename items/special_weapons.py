from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from .ranged_energy_weapon import RangedEnergyWeapon

import color
from actions import ActionResult
from random import randint, choice
import types
from . import WeaponType
from die_rollers import player_attack_roll

if TYPE_CHECKING:
    from magazine import Magazine
    from entities.enemy import Enemy
    from floor_map import FloorMap

def test_fire(self, target: Enemy, floor: FloorMap, **kwargs) -> None:
    hit_enemies = [target]
    self.owner.energy_points -= self.charge_needed
    if player_attack_roll(self, self.engine.player, self.calculate_distance_modifier(self.engine.player, target)):
        continue_chain = True
        while continue_chain:
            damage = self.roll_damage()
            target.take_damage(damage)
            if len(hit_enemies) == 1:
                self.engine.message_log.add_message(f"You hit the {target.name} for {damage} damage.", color.light_gray)
            else:
                self.engine.message_log.add_message(f"The lightning chains to {target.name} for {damage} damage.", color.light_gray)
            potential_targets = [t for t in floor.get_living_entities_in_radius(target.x, target.y, self.radius) if t not in hit_enemies]
            try:
                new_target = choice(potential_targets)
                hit_enemies.append(new_target)
                target = new_target
            except IndexError:
                continue_chain = False


    else:
        self.engine.message_log.add_message(f"You miss the {target.name}.", color.light_gray)

special_test = RangedEnergyWeapon(charge_needed = 12, die_count=3, damage_die=4, burst_count = 1, name="Lightning Cannon", hands = 2, optimal_range = 5, range_interval = 2, radius = 3, is_special = True)

special_test.fire = types.MethodType(test_fire, special_test)

