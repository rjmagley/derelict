from __future__ import annotations

from typing import Set, Iterable, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from entities.base_entity import BaseEntity
    from floor_map import FloorMap
    from input_handlers.event_handler import EventHandler

import numpy

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from actions.actions import EscapeAction, MovementAction
from entities.base_entity import BaseEntity
from entities.player import Player
from input_handlers import Handlers
from input_handlers.game_event_handler import GameEventHandler
from input_handlers.message_history_handler import MessageHistoryHandler
from floor_map import FloorMap
from messages import MessageLog
import tile_types
import color

# GameEngine - responsible for holding state of entire game - entities, maps,
# and so on, as well as drawing to console
class GameEngine():

    map: FloorMap
    event_handler: EventHandler
    context: Context

    def __init__(self, player: Player, root_console: Console, context: Context):
        self.event_handler = GameEventHandler(self)
        self.player = player
        self.message_log = MessageLog()
        self.map_console = Console(0, 0, order="F")
        self.message_console = Console(80, 4, order="F")
        self.status_console = Console(20, 20, order="F")
        self.root_console = root_console
        self.context = context

    def switch_handler(self, handler: Handlers):
        match handler:
            case Handlers.GAME_EVENT_HANDLER:
                self.event_handler = GameEventHandler(self)
            case Handlers.MESSAGE_HISTORY_HANDLER:
                self.event_handler = MessageHistoryHandler(self)

    def change_map(self, map) -> None:
        self.map = map
        self.map_console = Console(map.width, map.height, order="F")

    def handle_enemy_actions(self) -> None:
        for e in self.map.entities - {self.player}:
            if e.ai:
                e.ai.perform()

    def render(self) -> None:
        if type(self.event_handler) == GameEventHandler:
            self.update_fov()
            self.render_map(self.root_console)
            self.render_status(self.root_console)
            self.render_messages(self.root_console)
            self.context.present(self.root_console)
            self.root_console.clear()
        elif type(self.event_handler) == MessageHistoryHandler:
            self.render_message_history()

    def update_fov(self) -> None:
        self.map.visible[:] = compute_fov(
            self.map.tiles['transparent'],
            (self.player.x, self.player.y),
            radius=60
        )

        self.map.explored |= self.map.visible

    def render_map(self, root_console: Console) -> None:
        # get the player's X and Y values
        player_x, player_y = self.player.x, self.player.y

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
        elif player_x + 50 > self.map.width:
            render_x1 = self.map.width - 59
            render_x2 = self.map.width
        else:
            render_x1 = player_x - 10
            render_x2 = player_x + 50

        # print(f"{self.engine.player.x} {self.engine.player.y}")
        # print(f"render_x1: {render_x1} render_x2: {render_x2}")

        # grab the appropriate chunk of the map

        visible_section = self.map.visible[0:160, 0:20]
        explored_section = self.map.explored[0:160, 0:20]
        light_section = self.map.tiles['light'][0:160, 0:20]
        dark_section = self.map.tiles['dark'][0:160, 0:20]

        self.map_console.rgb[0:160, 0:20] = numpy.select(
            condlist=[visible_section, explored_section],
            choicelist=[light_section, dark_section],
            default=tile_types.unseen
        )

        sorted_entities = sorted((entity for entity in self.map.entities if self.map.visible[entity.x, entity.y]), key = lambda x: x.render_order.value)

        for e in sorted_entities:
            self.map_console.print(x=e.x, y=e.y, fg=e.color, string=e.char)

        self.map_console.blit(dest = root_console, dest_x = 0, dest_y = 0, src_x = render_x1, src_y = 0, width = 60, height = 20)

    def render_status(self, root_console: Console) -> None:
        # status window is 20x20 to the right of the playfield
        self.status_console.print(x = 0, y = 1, string = f"ARM: {self.player.hp}/{self.player.max_hp}", fg = color.white)
        self.status_console.blit(dest = root_console, dest_x = 59, dest_y = 0, width = 20, height = 20)

    def render_messages(self, root_console: Console) -> None:
        y_offset = 3

        for message, color in self.message_log.return_messages():
            self.message_console.print(0, y_offset, string=message, fg=color)
            y_offset -= 1
            if y_offset < 0:
                break

        self.message_console.blit(dest = root_console, dest_x = 0, dest_y = 20, width = 80, height = 4)
        self.message_console.clear()

    def render_message_history(self) -> None:
        y_offset = 22

        self.root_console.print(0, 0, string="Message History:")

        for message, color in self.message_log.return_messages():
            self.root_console.print(0, y_offset, string=message, fg=color)
            y_offset -= 1
            if y_offset < 2:
                break
        
        self.context.present(self.root_console)
        self.root_console.clear()