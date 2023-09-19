from __future__ import annotations

import string

from typing import Set, Iterable, Any, TYPE_CHECKING, Tuple

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
from input_handlers.game_event_handler import GameEventHandler
from input_handlers.message_history_handler import MessageHistoryHandler
from input_handlers.inventory_view_event_handler import InventoryViewEventHandler
from input_handlers.view_item_event_handler import ViewItemEventHandler

from items.base_weapon import BaseWeapon
from items.ranged_weapon import RangedWeapon

from floor_map import FloorMap
from messages import MessageLog
import tile_types
import color

# GameEngine - responsible for holding state of entire game - entities, maps,
# and so on, as well as drawing to console
class GameEngine():

    map: FloorMap
    event_handler: EventHandler | ViewItemEventHandler
    context: Context

    def __init__(self, player: Player, root_console: Console, context: Context):
        self.event_handler = GameEventHandler(self)
        self.player = player
        self.message_log = MessageLog()
        self.map_console = Console(0, 0, order="F")
        self.inventory_console = Console(60, 24, order="F")
        self.message_console = Console(80, 4, order="F")
        self.status_console = Console(20, 20, order="F")
        self.root_console = root_console
        self.context = context

    def switch_handler(self, handler, item = None):
        if item:
            self.event_handler = handler(self, item)
        else:
            self.event_handler = handler(self)

    def add_message(self, text: str, fg: Tuple[int, int, int] = color.white) -> None:
        self.message_log.add_message(text, fg)

    def change_map(self, map) -> None:
        self.map = map
        self.map_console = Console(map.width, map.height, order="F")

    def handle_enemy_actions(self) -> None:
        for e in self.map.living_entities:
            if e.ai:
                e.ai.perform()

    def render(self) -> None:
        # turns out you can't just reference a class in match/case statements
        # this is probably hacky as hell - the insances of each handler could
        # probably use an enum stating what kind of handler they are or
        # something - but this works for now

        # also that enum would reduce the number of imports hanging out up top,
        # that might be cool

        # all of these are getting self.root_console as an argument because
        # eventually they should hang out in a different file
        match type(self.event_handler).__name__:
            case GameEventHandler.__name__:
                self.update_fov()
                self.render_map(self.root_console)
                self.render_status(self.root_console)
                self.render_messages(self.root_console)
                self.context.present(self.root_console)
                self.root_console.clear()
            case MessageHistoryHandler.__name__:
                self.render_message_history()
            case InventoryViewEventHandler.__name__:
                self.render_status(self.root_console)
                self.render_inventory(self.root_console)
                self.context.present(self.root_console)
            case ViewItemEventHandler.__name__:
                if isinstance(self.event_handler.item, BaseWeapon):
                    self.render_weapon_description(self.root_console, self.event_handler.item)
                    self.context.present(self.root_console)

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
        self.status_console.print(x = 0, y = 0, string = f"Player Name", fg = color.white)
        self.status_console.print(x = 0, y = 1, string = f"ARM: {self.player.hp}/{self.player.max_hp}", fg = color.white)
        self.status_console.print(x = 0, y = 2, string = f"SHD: xxx/xxx", fg = color.white)
        self.status_console.print(x = 0, y = 3, string = f"PSY: xxx/xxx", fg = color.white)
        self.status_console.print(x = 0, y = 4, string = f"ENG: xxx/xxx", fg = color.white)

        self.status_console.print(x = 0, y = 6, string="Hands:", fg = color.white)
        if self.player.right_hand == None:
            self.status_console.print(x = 0, y = 7, string="Unarmed", fg = color.white)
        else:
            self.status_console.print(x = 0, y = 7, string=self.player.right_hand.status_string, fg = color.white)

        if self.player.left_hand == None:
            self.status_console.print(x = 0, y = 9, string="Unarmed", fg = color.white)
        else:
            self.status_console.print(x = 0, y = 9, string=self.player.left_hand.status_string, fg = color.white)

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
        y_offset = 23

        self.root_console.print(5, 0, string="Message History:")

        for message, color in self.message_log.return_messages():
            self.root_console.print(0, y_offset, string=message, fg=color)
            y_offset -= 1
            if y_offset < 2:
                break
        
        self.context.present(self.root_console)
        self.root_console.clear()

    def render_inventory(self, root_console: Console) -> None:

        self.inventory_console.print(5, 0, string="Inventory:")

        y_offset = 2
        for item, letter in zip(self.player.inventory.items, string.ascii_lowercase):
            self.inventory_console.print(5, y_offset, string=f"{letter} - {item.name}")
            y_offset += 1

        self.inventory_console.blit(dest = root_console, dest_x = 0, dest_y = 0, width = 59, height = 20)
        self.inventory_console.clear()

    # am I really going to write a method for each one of these?
    # wouldn't it make sense to have one function that generates a block of text
    # for this? christ
    def render_weapon_description(self, root_console: Console, item) -> None:
        
        self.inventory_console.print(5, 1, string=f"{item.name} - {item.hands}-handed weapon")
        damage_string = f"Damage: {item.damage_die}d{item.die_count}"
        if isinstance(item, RangedWeapon):
            damage_string += f" - fires in {item.burst_count}-round burst"
        self.inventory_console.print(5, 3, string=damage_string)

        y_offset = 5

        if isinstance(item, RangedWeapon):
            self.inventory_console.print(5, y_offset, string=f"{item.loaded_ammo} of {item.magazine_size} in magazine")
            y_offset += 2

        if item.description:
            self.inventory_console.print(5, y_offset, string=item.description)
            y_offset += 1

        self.inventory_console.blit(dest = root_console, dest_x = 0, dest_y = 0, width = 59, height = 20)
        self.inventory_console.clear()