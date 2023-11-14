from __future__ import annotations

from typing import TYPE_CHECKING

import color

if TYPE_CHECKING:
    from tcod.console import Console
    from entities.player import Player

def render_character_profile(root_console: Console, center_console: Console, player: Player) -> None:

    center_console.print(x=1, y=1, string=f"Character Information for {player.name}", fg=color.white)

    center_console.print(x=1, y=3, string=f"Equipped Weapons:", fg=color.white)

    left_offset = 5

    for w in (w for w in player.equipped_weapons if w != None):
        center_console.print(x=1, y=left_offset, string=f"{w.name}\n{w.status_string}", fg=color.white)
        left_offset += 3

    center_console.print(x=1, y=left_offset, string=f"Available Powers:", fg=color.white)    
    left_offset += 1
    
    for p in player.powers:
        center_console.print(x=1, y=left_offset, string=f"{p.name} - {p.power_cost}", fg=color.white)
        left_offset += 1

    center_console.blit(dest = root_console, dest_x = 0, dest_y = 0, width = 60, height = 20)
    center_console.clear()