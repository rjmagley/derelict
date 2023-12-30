from __future__ import annotations

import string
import time

from typing import Set, Iterable, Any, TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from entities.base_entity import BaseEntity
    from floor_map import FloorMap
    from input_handlers.event_handler import EventHandler
    from items.magazine import Magazine

import numpy

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov
from tcod import constants

from renderers import *

from actions.actions import EscapeAction, MovementAction
from entities.base_entity import BaseEntity
from entities.player import Player
from input_handlers import HandlerType, provide_handler
from items import AmmunitionType
from items.base_weapon import BaseWeapon
from items.base_armor import BaseArmor
from items.ranged_weapon import RangedWeapon
from input_handlers.game_event_handler import GameEventHandler
from floor_generation.floor_generation import generate_floor

from floor_map import FloorMap
from messages import MessageLog
import tile_types
import color



# GameEngine - responsible for holding state of entire game - entities, maps,
# and so on, as well as drawing to console
# the drawing bits might be better off in another class
class GameEngine():

    map: FloorMap
    event_handler: EventHandler
    context: Context

    def __init__(self, player: Player, root_console: Console, context: Context):
        self.event_handler = GameEventHandler(self)
        self.player = player
        self.message_log = MessageLog()
        self.center_console = Console(0, 0, order="F")
        self.inventory_console = Console(60, 24, order="F")
        self.bottom_console = Console(80, 4, order="F")
        self.side_console = Console(20, 20, order="F")
        self.root_console = root_console
        self.context = context
        self.dying_entities = []
        self.difficulty_level = 1
        self.auts_elapsed = 0

    def game_loop(self):
        self.render()
        # self.handle_turns()
        self.check_player_turn()
        self.check_enemy_turns()
        for e in self.map.living_entities:
            e.periodic_refresh()
        
        self.handle_deaths()

        self.auts_elapsed += 1

    def check_player_turn(self):
        
        self.player.delay -= 1
        if self.player.delay <= 0:
            turn_passed = False
            while turn_passed != True:
                self.render()
                self.update_fov()
                action_result = self.event_handler.handle_events()
                if action_result == None:
                    continue
                elif action_result.time_passed:
                    turn_passed = True
                    self.player.delay += action_result.time_taken
                if action_result.message:
                    self.add_message(action_result.message, action_result.message_color)

    def check_enemy_turns(self):
        for e in [e for e in self.map.awake_entities if e != self.player]:
            e.delay -= 1
            if e.ai:
                # print(f"{e.name} - {e.delay}")
                if e.delay <= 0:
                    action_result = e.ai.perform()
                    if action_result.time_passed:
                        e.delay += action_result.time_taken
                    if action_result.message:
                        self.add_message(action_result.message, action_result.message_color)


    def switch_handler(self, handler, **kwargs) -> None:
        print(f"switching handler to {handler}")
        self.event_handler = provide_handler(handler)(self, **kwargs)

    def add_message(self, text: str, fg: Tuple[int, int, int] = color.white) -> None:
        self.message_log.add_message(text, fg)

    def change_map(self, map) -> None:
        self.map = map
        self.center_console = Console(map.width, map.height, order="F")
    
    # def handle_turns(self) -> None:
    #     # now that the player can move and act faster/slower than normal,
    #     # this messes with the periodic refresh call
    #     # this may be time to move this logic out of turn-handling and into
    #     # a seperate function
    #     if self.player.delay % 10 == 0:
    #         self.player.periodic_refresh()
    #     if self.player.delay <= 0:
            

        
    #     self.player.delay -= 1
        
    #     self.update_fov()
    #     self.handle_deaths()


    def render(self) -> None:

        # starting to wonder if this bundle of switch/case statements wouldn't
        # be better off just living in the handler classes themselves
        match self.event_handler.handler_type:
            case HandlerType.GAME:
                self.update_fov()
                render_map(self.root_console, self.center_console, self.player, self.map)
                render_status_side(self.root_console, self.side_console, self.player)
                render_messages_bottom(self.root_console, self.bottom_console, self.message_log)

            case HandlerType.MESSAGE_HISTORY:
                render_message_history(self.root_console, self.message_log)

            case HandlerType.INVENTORY_VIEW:
                render_status_side(self.root_console, self.side_console, self.player)
                render_inventory(self.root_console, self.inventory_console, self.event_handler)

            case HandlerType.ITEM_VIEW:
                if isinstance(self.event_handler.item, BaseWeapon):
                    render_weapon_description(self.root_console, self.inventory_console, self.event_handler.item, self.player)
                    self.context.present(self.root_console)
                elif isinstance(self.event_handler.item, BaseArmor):
                    render_armor_description(self.root_console, self.inventory_console, self.event_handler.item, self.player)
                    self.context.present(self.root_console)

            # looking is very incomplete - shows no information really
            case HandlerType.LOOK:
                render_map(self.root_console, self.center_console, self.player, self.map)
                render_map_cursor(self.root_console, self.center_console, self.map, self.event_handler, self.player)
                render_status_side(self.root_console, self.side_console, self.player)

            case HandlerType.TARGETING:
                render_map(self.root_console, self.center_console, self.player, self.map)
                render_map_cursor(self.root_console, self.center_console, self.map, self.event_handler, self.player)
                render_status_side(self.root_console, self.side_console, self.player)
                render_targeting_information(self.root_console, self.bottom_console, self.event_handler.weapon, self, self.map)

            case HandlerType.POWER_TARGETING:
                render_map(self.root_console, self.center_console, self.player, self.map)
                render_map_cursor(self.root_console, self.center_console, self.map, self.event_handler, self.player)
                render_status_side(self.root_console, self.side_console, self.player)
                render_targeting_information(self.root_console, self.bottom_console, self.event_handler.power, self, self.map)

            case HandlerType.CHARACTER_PROFILE:
                render_character_profile(self.root_console, self.center_console, self.player)
                render_status_side(self.root_console, self.side_console, self.player)
                render_messages_bottom(self.root_console, self.bottom_console, self.message_log)

            case HandlerType.POWER_LIST:
                render_power_list(self.root_console, self.inventory_console, self.player)
                render_status_side(self.root_console, self.side_console, self.player)

            case HandlerType.WEAPON_SELECT:
                render_weapon_selector(self.root_console, self.bottom_console, self.player)
                render_map(self.root_console, self.center_console, self.player, self.map)
                render_status_side(self.root_console, self.side_console, self.player)

            case HandlerType.INTERMISSION:
                render_intermission(self.root_console, self.event_handler)



        self.context.present(self.root_console)
        self.root_console.clear()
    
    # changing the FOV code to be a little more restrictive so that enemies
    # around corners aren't visible - also, should this even be in the engine?
    # should it live in the map?
    def update_fov(self) -> None:
        self.map.visible[:] = compute_fov(
            self.map.tiles['transparent'],
            (self.player.x, self.player.y),
            radius=self.player.vision_radius,
            algorithm=constants.FOV_SHADOW
        )

        sleepers = self.map.asleep_entities
        for e in sleepers:
            if self.map.visible[e.x, e.y]:
                e.awake = True

        self.map.explored |= self.map.visible

    def handle_deaths(self) -> None:
        for e in self.dying_entities:
            if e.is_alive:
                self.player.on_enemy_death(e)
                e.die()

        self.dying_entities = []

    def advance_map(self) -> None:
        self.difficulty_level += 1
        self.map = generate_floor(160, 20, self, self.difficulty_level)
        self.message_log.add_message(f"Welcome... to level {self.difficulty_level}!", color.magenta)

        # when the map changes, the player's shield is refreshed and their psy
        # points are refilled
        self.player.shield_points = self.player.max_shield
        self.player.psy_points = self.player.max_psy