from __future__ import annotations

from typing import TYPE_CHECKING

from random import randint

if TYPE_CHECKING:
    from items.base_weapon import BaseWeapon
    from entities.player import Player

# standard roll does 3d6, returns True if result is under target
def standard_roll_target(target: int, modifier: int = 0) -> bool:
    result = 0
    for i in range(0, 3):
        result += randint(1, 6)
    return result <= target

def roll_dice(number_dice: int, number_sides: int) -> int:
    result = 0
    for i in range(0, number_dice):
        result += randint(1, number_sides)
    return result

def player_attack_roll(weapon: BaseWeapon, player: Player, modifier: int = 0) -> bool:
    target = player.player_stats[weapon.weapon_type]
    roll = roll_dice(3, 6) + modifier
    return roll <= target

def enemy_attack_roll(weapon_skill: int, modifier: int = 0) -> bool:
    target = weapon_skill
    roll = roll_dice(3, 6) + modifier
    return roll <= target