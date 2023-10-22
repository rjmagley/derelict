from __future__ import annotations

import string

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tcod.console import Console
    from input_handlers.inventory_view_event_handler import InventoryViewEventHandler


def render_inventory(root_console: Console, inventory_console: Console, handler: InventoryViewEventHandler) -> None:

    inventory_console.print(1, 0, string="Inventory:")

    inventory_console.print(1, 2, string="Weapons:")
    y_offset = 4
    if len(handler.weapons_dictionary) == 0:
        inventory_console.print(1, 4, string="No weapons\nin inventory")

    else:
        for k, v in handler.weapons_dictionary.items():
            inventory_console.print(1, y_offset, string=f"{k} - {v.name}")
            y_offset += 1

    inventory_console.print(30, 2, string="Armor:")
    y_offset = 4
    if True:
    # if len(handler.weapons_dictionary) == 0: - this will check armor someday
        inventory_console.print(30, 4, string="No armor\nin inventory")

    else:
        for k, v in handler.weapons_dictionary.items():
            inventory_console.print(1, y_offset, string=f"{k} - {v.name}")
            y_offset += 1

    inventory_console.blit(dest = root_console, dest_x = 0, dest_y = 0, width = 59, height = 20)
    inventory_console.clear()