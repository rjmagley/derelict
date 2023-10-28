from __future__ import annotations

from typing import TYPE_CHECKING, Union

from tcod.console import Console
from items.ranged_weapon import RangedWeapon
from powers.base_power import BasePower
from entities.player import Player
from floor_map import FloorMap
import color

if TYPE_CHECKING:
    from game_engine import GameEngine

def render_targeting_information(root_console: Console, bottom_console: Console,targeter: RangedWeapon | BasePower, engine: GameEngine, map: FloorMap) -> None:
    target = map.get_blocking_entity_at_location(engine.event_handler.x, engine.event_handler.y)
    if target:
        bottom_console.print(x=0, y=1, fg=color.white, string=f"Aiming at {target.name} ({target.x}, {target.y})")
    else:
        bottom_console.print(x=0, y=1, fg=color.light_gray, string=f"Nothing here. ({engine.event_handler.x} {engine.event_handler.y})")
    if isinstance(targeter, RangedWeapon):
        targeter_string=f"Targeting with your {targeter.name}"
        if target:
            targeter_string += f" modifier is {targeter.calculate_distance_modifier(engine.player, target)}"
        bottom_console.print(x=0, y=0, fg=color.white, string=targeter_string)
    elif isinstance(targeter, BasePower):
        bottom_console.print(x=0, y=0, fg=color.white, string=f"Targeting your {targeter.name} power")


    message = engine.message_log.return_last_message()
    bottom_console.print(x=0, y=3, fg=message[1], string=message[0])

    bottom_console.blit(dest = root_console, dest_x = 0, dest_y = 20, width = 80, height = 4)
    bottom_console.clear()