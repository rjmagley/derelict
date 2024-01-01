from __future__ import annotations

from typing import TYPE_CHECKING, Type

import color
import math

from tcod.los import bresenham

from .player_map_offset import player_map_offset

if TYPE_CHECKING:
    from tcod.console import Console
    from entities.player import Player
    from floor_map import FloorMap
    from input_handlers.event_handler import EventHandler

def render_map_cursor(root_console: Console, center_console: Console, map: FloorMap, handler: EventHandler, player: Player) -> None:

    # creates a Bresenham line to the target
    # this currently will clip through a wall, even if the enemy is visible
    # per the FOV (like around a corner) - may need to try to jiggle this 
    # around to get around that? 

    # for now I'm going to change the FOV to make it so that an enemy just
    # around a corner can't be seen - would like to restore that, though
    # maybe the doomRL source has answers?
    # or maybe I can implement a light "cover" system - if enemy is in FOV but
    # a corner is in the way, allow the shot but with a penalty?
    points = bresenham((player.x, player.y), (handler.x, handler.y)).tolist()

    draw_color = color.green
    for p in points[1:-1]:
        if map.tiles['blocking'][p[0], p[1]]:
            draw_color = color.red
        center_console.print(x = p[0], y = p[1], fg = draw_color, string='*')

    center_console.print(x = handler.x, y = handler.y, fg = color.white, string='X')
    if hasattr(handler, 'radius'):
        for x in range(handler.x - handler.radius + 1, handler.x+handler.radius):
            for y in range(handler.y - handler.radius + 1, handler.y+handler.radius):
                if map.in_bounds(x, y):
                    center_console.bg[x, y] = color.red
    center_console.blit(dest = root_console, src_x = player_map_offset(player, map), width = 60, height = 20)
    
    center_console.clear()