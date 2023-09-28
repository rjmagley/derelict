from __future__ import annotations

from typing import TYPE_CHECKING

from random import randint

if TYPE_CHECKING:
    from items.base_weapon import BaseWeapon
    from entities.player import Player

def roll_dice(number_sides: int, number_dice: int) -> int:
    result = 0
    for i in range(0, number_dice):
        result += randint(1, number_sides)
    return result

def player_attack_roll(weapon: BaseWeapon, player: Player) -> bool:
    print(weapon.weapon_type)
    target = player.player_stats[weapon.weapon_type]
    print(target)
    roll = roll_dice(3, 6)
    return roll <= target