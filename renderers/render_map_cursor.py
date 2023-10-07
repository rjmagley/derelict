from __future__ import annotations

from typing import TYPE_CHECKING, Type

import color

from .player_map_offset import player_map_offset

if TYPE_CHECKING:
    from tcod.console import Console
    from entities.player import Player
    from floor_map import FloorMap
    from input_handlers.event_handler import EventHandler

def render_map_cursor(root_console: Console, center_console: Console, map: FloorMap, handler: EventHandler, player: Player) -> None:


    center_console.print(x = handler.x, y = handler.y, fg = color.white, string='X')
    if hasattr(handler, 'radius'):
        print(f"radius: {handler.radius}")
        for x in range(handler.x - handler.radius + 1, handler.x+handler.radius):
            for y in range(handler.y - handler.radius + 1, handler.y+handler.radius):
                print(x, y)
                center_console.bg[x, y] = color.red
    center_console.blit(dest = root_console, src_x = player_map_offset(player, map), width = 60, height = 20)
    
    center_console.clear()