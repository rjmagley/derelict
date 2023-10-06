import numpy

from .player_map_offset import player_map_offset

import tile_types
from tcod.console import Console
from entities.player import Player
from floor_map import FloorMap

def render_map(root_console: Console, center_console: Console, player: Player, map: FloorMap) -> None:


    # the map renders ten columns behind the player and fifty ahead of them
    # (the player is included in that fifty)
    # combat is intended to include very long ranges, and the game's intent
    # is for the player to methodically clear out what's ahead of them
    # moving left to right - they can skip past enemies, but they might
    # be shooting the player in the back!

    # render_x1 is where the first column of the screen will start
    # if the player is hugging the left wall, we don't want to try to render
    # negative x values

    # render_x2 is the last column of the screen - again, we want to make
    # sure we don't try to pull up map data outside the map bounds

    # there are three possibilities:
    # player is too close to left wall - start rendering the map from
    # column 0 to column 59
    # player is too close to right wall - start rendering the map from
    # column (map.width - 61) to column (map.width)
    # player is in the middle of the map - just get render_x1 and render_x2
    # by modifying the player x position


    # print(f"{self.engine.player.x} {self.engine.player.y}")
    # print(f"render_x1: {render_x1} render_x2: {render_x2}")

    # grab the appropriate chunk of the map

    visible_section = map.visible[0:160, 0:20]
    explored_section = map.explored[0:160, 0:20]
    light_section = map.tiles['light'][0:160, 0:20]
    dark_section = map.tiles['dark'][0:160, 0:20]

    center_console.rgb[0:160, 0:20] = numpy.select(
        condlist=[visible_section, explored_section],
        choicelist=[light_section, dark_section],
        default=tile_types.unseen
    )

    sorted_entities = sorted((entity for entity in map.entities if map.visible[entity.x, entity.y]), key = lambda x: x.render_order.value)

    for e in sorted_entities:
        center_console.print(x=e.x, y=e.y, fg=e.color, string=e.char)

    center_console.blit(dest = root_console, dest_x = 0, dest_y = 0, src_x = player_map_offset(player, map), width = 60, height = 20)

    