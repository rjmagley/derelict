from __future__ import annotations

from typing import TYPE_CHECKING

import color

if TYPE_CHECKING:
    from tcod.console import Console
    from entities.player import Player

def render_character_profile(root_console: Console, player: Player) -> None:

    root_console.print(x=0, y=0, string=f"Character Information for {player.name}", fg=color.white)