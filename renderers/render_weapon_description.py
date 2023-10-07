from tcod.console import Console
from items.base_item import BaseItem
from items.ranged_weapon import RangedWeapon
from entities.player import Player

# am I really going to write a method for each one of these?
# wouldn't it make sense to have one function that generates a block of text
# for this? christ

def render_weapon_description(root_console: Console, inventory_console: Console,item: BaseItem, player: Player) -> None:
        
    y_offset = 3

    inventory_console.print(5, 1, string=f"{item.name} - {item.hands}-handed weapon")
    damage_string = f"Damage: {item.die_count}d{item.damage_die}"
    if isinstance(item, RangedWeapon):
        if item.burst_count > 1:
            damage_string += f" - fires in {item.burst_count}-round burst"
    inventory_console.print(5, y_offset, string=damage_string)

    y_offset += 1

    if item.description:
        inventory_console.print(5, y_offset, string=item.description)
        y_offset += 1

    if isinstance(item, RangedWeapon):
        inventory_console.print(5, y_offset, string=f"{item.loaded_ammo} of {item.magazine_size} in magazine")
        y_offset += 1

    if player.has_equipped(item):
        inventory_console.print(5, y_offset, string=f"{item.name} is in your hand{'s' if item.hands == 2 else ''}")
    else:
        inventory_console.print(5, y_offset, string=f"Press 'e' to equip the {item.name}")
    

    inventory_console.blit(dest = root_console, dest_x = 0, dest_y = 0, width = 59, height = 24)
    inventory_console.clear()