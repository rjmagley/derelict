import string

from tcod.console import Console
from entities.player import Player

import color


def render_power_list(root_console: Console, inventory_console: Console, player: Player) -> None:

    inventory_console.print(1, 0, string="Powers:")

    y_offset = 2
    for power, letter in zip(player.powers, string.ascii_lowercase):
        inventory_console.print(1, y_offset, string=f"{letter} - {power.name} ({power.power_cost})", fg = color.white if power.can_cast else color.light_gray)
        y_offset += 1

    inventory_console.blit(dest = root_console, dest_x = 0, dest_y = 0, width = 59, height = 20)
    inventory_console.clear()