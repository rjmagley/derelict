from tcod.console import Console
from items.base_item import BaseItem
from items.base_armor import BaseArmor
from entities.player import Player

# starting to wonder if this should all be one function, or broken into helpers,
# or if I should have a function that just splits out a block of text

def render_armor_description(root_console: Console, inventory_console: Console, 
    armor: BaseArmor, player: Player) -> None:

    y_offset = 3

    inventory_console.print(5, 1, string=f"{armor.name} ({armor.armor_type})")

    if armor.description:
        inventory_console.print(5, y_offset, string=armor.description)
        y_offset += 1

    inventory_console.print(5, y_offset+1, string=f"Basic stats:")
    inventory_console.print(5, y_offset+2, string=f"AP: {armor.max_armor_points} | DR: {armor.damage_resist}")

    y_offset += 2

    if len(armor.properties) != 0:
        inventory_console.print(5, y_offset+1, string=f"Properties:")
        for k, v in armor.properties.items():
            y_offset += 1
            inventory_console.print(5, y_offset+1, string=f"{k} - {'-' if v < 0 else ''}{v}")


    inventory_console.blit(dest = root_console, dest_x = 0, dest_y = 0, width = 59, height = 24)
    inventory_console.clear()