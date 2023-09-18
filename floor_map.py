from __future__ import annotations

from typing import Iterable, TYPE_CHECKING, List, Set

import numpy
import tile_types

from tcod.console import Console

from entities.combatant import Combatant

if TYPE_CHECKING:
    from entities.base_entity import BaseEntity
    from game_engine import GameEngine

# FloorMap - contains all the data for a given floor, including its layout
# should also probably contain its entities if we want the player to be able to
# go up and down floors at will
class FloorMap():
    def __init__(self, engine: GameEngine, width: int, height: int, entities: Iterable[BaseEntity] = {}) -> None:
        self.engine = engine
        self.width = width
        self.height = height
        self.entities = entities
        self.tiles = numpy.full((width, height), fill_value=tile_types.wall, order="F")

        self.visible = numpy.full((width, height), fill_value=False, order='F')
        self.explored = numpy.full((width, height), fill_value=False, order='F')
        self.map_console = Console(width, height, order="F")

    @property
    def living_entities(self) -> Set[BaseEntity]:
        yield from (e for e in self.entities if isinstance(e, Combatant) and e.is_alive)

    def get_entities_at_location(self, x: int, y: int) -> Optional[BaseEntity]:
        
        result = []
        
        for e in self.entities:
            if e.x == x and e.y == y:
                result.append(e)

        return sorted(result, key = lambda x: x.render_order.value)

    def get_blocking_entity_at_location(self, x: int, y: int) -> Optional[BaseEntity]:

        for e in self.entities:
            if e.x == x and e.y == y and e.blocks_movement == True:
                return e

        return None

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    # original render function 
    # def render(self, console: Console) -> None:
    #     console.rgb[0:self.width, 0:self.height] = numpy.select(
    #         condlist=[self.visible, self.explored],
    #         choicelist=[self.tiles['light'], self.tiles['dark']],
    #         default=tile_types.unseen
    #     )
    #     for e in (entity for entity in self.entities if self.visible[entity.x, entity.y]):
    #         console.print(x=e.x, y=e.y, fg=e.color, string=e.char)

    def render(self, root_console: Console) -> None:
        # get the player's X and Y values
        player_x, player_y = self.engine.player.x, self.engine.player.y

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
        if player_x < 10:
            render_x1 = 0
            render_x2 = 60
        elif player_x + 50 > self.width:
            render_x1 = self.width - 59
            render_x2 = self.width
        else:
            render_x1 = player_x - 10
            render_x2 = player_x + 50

        print(f"{self.engine.player.x} {self.engine.player.y}")
        print(f"render_x1: {render_x1} render_x2: {render_x2}")

        # grab the appropriate chunk of the map

        visible_section = self.visible[0:160, 0:20]
        print(visible_section.shape)
        explored_section = self.visible[0:160, 0:20]
        light_section = self.tiles['light'][0:160, 0:20]
        print(light_section.shape)
        dark_section = self.tiles['dark'][0:160, 0:20]
        print(dark_section.shape)

        self.map_console.rgb[0:160, 0:20] = numpy.select(
            condlist=[visible_section, explored_section],
            choicelist=[light_section, dark_section],
            default=tile_types.unseen
        )

        sorted_entities = sorted((entity for entity in self.entities if self.visible[entity.x, entity.y]), key = lambda x: x.render_order.value)

        for e in sorted_entities:
            self.map_console.print(x=e.x, y=e.y, fg=e.color, string=e.char)
            print(f"rendering {e.name} at {e.x} {e.y}")

        self.map_console.blit(dest = root_console, dest_x = 0, dest_y = 0, src_x = render_x1, src_y = 0, width = 60, height = 20)