from __future__ import annotations

from typing import TYPE_CHECKING, Type

import color

from items import AmmunitionType

if TYPE_CHECKING:
    from tcod.console import Console
    from entities.player import Player
    from floor_map import FloorMap
    from input_handlers.event_handler import EventHandler
    from items.magazine import Magazine

def render_status_side(root_console: Console, side_console: Console, player: Player):

    magazine: Magazine = player.magazine

    side_console.print(x = 0, y = 0, string = f"{player.x}, {player.y}", fg = color.white)
    side_console.print(x = 16, y = 0, string = "Ammo", fg = color.white)
    side_console.print(x = 0, y = 1, string = f"ARM: {player.armor_points}/{player.max_armor}", fg = color.white)
    side_console.print(x = 15, y = 1, string = f"L:{magazine.get_percentage(AmmunitionType.LIGHT)}", fg = color.light_gray)
    side_console.print(x = 0, y = 2, string = f"SHD: {player.get_shield_status()}", fg = color.bright_cyan)
    side_console.print(x = 15, y = 2, string = f"H:{magazine.get_percentage(AmmunitionType.HEAVY)}", fg = color.white)
    side_console.print(x = 0, y = 3, string = f"PSY: {player.get_psy_status()}", fg = color.bright_magenta)
    side_console.print(x = 15, y = 3, string = f"E:{magazine.get_percentage(AmmunitionType.EXPLOSIVE)}", fg = color.yellow)
    side_console.print(x = 0, y = 4, string = f"ENG: {player.get_energy_status()}", fg = color.bright_blue)
    side_console.print(x = 15, y = 4, string = f"X:{magazine.get_percentage(AmmunitionType.EXOTIC)}", fg = color.magenta)

    side_console.print(x = 0, y = 6, string="Hands:", fg = color.white)
    if player.right_hand == None:
        side_console.print(x = 0, y = 7, string="Unarmed", fg = color.white)
    else:
        side_console.print(x = 0, y = 7, string=player.right_hand.name, fg = color.white)
        side_console.print(x = 0, y = 8, string=f"{player.right_hand.status_string}", fg = color.white)

    if not player.twohanded_weapon:
        if player.left_hand == None:
            side_console.print(x = 0, y = 9, string="-----", fg = color.white)
        else:
            side_console.print(x = 0, y = 9, string=player.left_hand.name, fg = color.white)
            side_console.print(x = 0, y = 10, string=f"{player.left_hand.status_string}", fg = color.white)

    side_console.print(x = 0, y = 12, string="Shoulders:", fg = color.white)
    if player.right_shoulder == None:
        side_console.print(x = 0, y = 13, string="-----", fg = color.white)
    else:
        side_console.print(x = 0, y = 13, string=player.right_shoulder.name, fg = color.white)
        side_console.print(x = 0, y = 14, string=f"{player.right_shoulder.status_string}", fg = color.white)

    if player.left_shoulder == None:
        side_console.print(x = 0, y = 15, string="-----", fg = color.white)
    else:
        side_console.print(x = 0, y = 15, string=player.left_shoulder.name, fg = color.white)
        side_console.print(x = 0, y = 16, string=f"{player.left_shoulder.status_string}", fg = color.white)

    side_console.blit(dest = root_console, dest_x = 60, dest_y = 0, width = 20, height = 20)
    side_console.clear()