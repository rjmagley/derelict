from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.console import Console
from items.ranged_weapon import RangedWeapon
from entities.player import Player
from floor_map import FloorMap
import color

if TYPE_CHECKING:
    from game_engine import GameEngine

def render_targeting_information(root_console: Console, bottom_console: Console,weapon: RangedWeapon, engine: GameEngine, map: FloorMap) -> None:
    bottom_console.print(x=0, y=0, fg=color.white, string=f"Targeting with your {weapon.name}")
    target = map.get_blocking_entity_at_location(engine.event_handler.x, engine.event_handler.y)
    if target:
        bottom_console.print(x=0, y=1, fg=color.white, string=f"Aiming at {target.name}")
    else:
        bottom_console.print(x=0, y=1, fg=color.light_gray, string=f"Nothing here.")

    message = engine.message_log.return_last_message()
    bottom_console.print(x=0, y=3, fg=message[1], string=message[0])

    bottom_console.blit(dest = root_console, dest_x = 0, dest_y = 20, width = 80, height = 4)
    bottom_console.clear()