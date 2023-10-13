from __future__ import annotations

from typing import TYPE_CHECKING, Union

from tcod.console import Console
from items.ranged_weapon import RangedWeapon
from powers.base_power import BasePower
from floor_map import FloorMap
import color

if TYPE_CHECKING:
    from game_engine import GameEngine
    from entities.player import Player

def render_weapon_selector(root_console: Console, bottom_console: Console, player: Player):
    weapons = [w for w in player.equipped_weapons if w != None]
    print(weapons)

    bottom_console.print(x=0, y=0, fg=color.white, string=f"Select a weapon to fire:")
    for i in range(0, len(weapons)):
        bottom_console.print(x=25, y=i, fg=color.white, string=f"{i+1} - {weapons[i].name}")

    bottom_console.blit(dest = root_console, dest_x = 0, dest_y = 20, width = 80, height = 4)
    bottom_console.clear()   