import string

from tcod.console import Console
from entities.player import Player


def render_inventory(root_console: Console, inventory_console: Console, player: Player) -> None:

    inventory_console.print(1, 0, string="Inventory:")

    y_offset = 2
    for item, letter in zip(player.inventory.items, string.ascii_lowercase):
        inventory_console.print(1, y_offset, string=f"{letter} - {item.name}")
        y_offset += 1

    inventory_console.blit(dest = root_console, dest_x = 0, dest_y = 0, width = 59, height = 20)
    inventory_console.clear()