from __future__ import annotations

from typing import TYPE_CHECKING

import color

if TYPE_CHECKING:
    from tcod.console import Console
    from input_handlers.intermission_handler import IntermissionEventHandler

def render_intermission(intermission_console: Console, handler: IntermissionEventHandler) -> None:

    intermission_console.print(1, 0, string="Intermission - Progressing To (level name?)")
    intermission_console.print(1, 1, string="Press the key listed for each shoulder weapon or armor category to select\nwhich item to interact with")
    intermission_console.print(1, 3, string="Shift+key to equip that item in place of the current selection")
    intermission_console.print(1, 4, string="Ctrl+key to select that item for dropping - it'll be gone forever!")
    intermission_console.print(1, 5, string="Grey background means item is selected - red means it will be dropped")

    # divided up into 3 columns
    # first column - shoulders and magazine

    intermission_console.print(1, 7, string="L - Left shoulder")
    y_offset = 7
    for w in handler.inventory_items['left_shoulder']:
        if w in handler.items_to_drop['left_shoulder']:
            bg_color = color.red
        else:
            bg_color = color.dark_gray if w == handler.chosen_items['left_shoulder'] else color.black
        if w == None:
            intermission_console.print(1, y_offset+1, string=f"> None" if handler.inventory_items['left_shoulder'].index(w) == handler.current_index['left_shoulder'] else f"None",
            bg = bg_color)
        else:
            intermission_console.print(1, y_offset+1, string=f"> {w.name}" if handler.inventory_items['left_shoulder'].index(w) == handler.current_index['left_shoulder'] else f"{w.name}",
            bg = bg_color)
        y_offset += 1

    y_offset += 2

    intermission_console.print(1, y_offset, string="R - Right shoulder")
    for w in handler.inventory_items['right_shoulder']:
        if w in handler.items_to_drop['right_shoulder']:
            bg_color = color.red
        else:
            bg_color = color.dark_gray if w == handler.chosen_items['right_shoulder'] else color.black
        if w == None:
            intermission_console.print(1, y_offset+1, string=f"> None" if handler.inventory_items['right_shoulder'].index(w) == handler.current_index['right_shoulder'] else f"None",
            bg = bg_color)
        else:
            intermission_console.print(1, y_offset+1, string=f"> {w.name}" if handler.inventory_items['right_shoulder'].index(w) == handler.current_index['right_shoulder'] else f"{w.name}",
            bg = bg_color)
        y_offset += 1

    y_offset += 2

    intermission_console.print(1, y_offset, string="M - Magazine")
    for m in handler.inventory_items['magazine']:
        if m in handler.items_to_drop['magazine']:
            bg_color = color.red
        else:
            bg_color = color.dark_gray if m == handler.chosen_items['magazine'] else color.black
        intermission_console.print(1, y_offset+1, string=f"> {m.name}" if handler.inventory_items['magazine'].index(m) == handler.current_index['magazine'] else f"{m.name}",
        bg = bg_color)
        y_offset += 1

    # second column: helmets, chestplates and arms
    y_offset = 7
    intermission_console.print(26, 7, string="H - Helmet")
    for h in handler.inventory_items['helmet']:
        if h in handler.items_to_drop['helmet']:
            bg_color = color.red
        else:
            bg_color = color.dark_gray if h == handler.chosen_items['helmet'] else color.black
        intermission_console.print(26, y_offset+1, string=f"> {h.name}" if handler.inventory_items['helmet'].index(h) == handler.current_index['helmet'] else f"{h.name}",
        bg = bg_color)
        y_offset += 1

    y_offset += 2

    intermission_console.print(26, y_offset, string="C - Chest")
    for c in handler.inventory_items['chest']:
        if c in handler.items_to_drop['chest']:
            bg_color = color.red
        else:
            bg_color = color.dark_gray if c == handler.chosen_items['chest'] else color.black
        intermission_console.print(26, y_offset+1, string=f"> {c.name}" if handler.inventory_items['chest'].index(c) == handler.current_index['chest'] else f"{c.name}",
        bg = bg_color)
        y_offset += 1

    y_offset += 2

    intermission_console.print(26, y_offset, string="A - Arms")
    for a in handler.inventory_items['arms']:
        if a in handler.items_to_drop['arms']:
            bg_color = color.red
        else:
            bg_color = color.dark_gray if a == handler.chosen_items['arms'] else color.black
        intermission_console.print(26, y_offset+1, string=f"> {a.name}" if handler.inventory_items['arms'].index(a) == handler.current_index['arms'] else f"{a.name}",
        bg = bg_color)
        y_offset += 1

    # third column: legs, backpacks and shields
    
    y_offset = 7

    intermission_console.print(51, 7, string="E - lEgs")
    for l in handler.inventory_items['legs']:
        if l in handler.items_to_drop['legs']:
            bg_color = color.red
        else:
            bg_color = color.dark_gray if l == handler.chosen_items['legs'] else color.black
        intermission_console.print(51, y_offset+1, string=f"> {l.name}" if handler.inventory_items['legs'].index(l) == handler.current_index['legs'] else f"{l.name}",
        bg = bg_color)
        y_offset += 1

    y_offset += 2

    intermission_console.print(51, y_offset, string="B - Backpack")
    for b in handler.inventory_items['backpack']:
        if b in handler.items_to_drop['backpack']:
            bg_color = color.red
        else:
            bg_color = color.dark_gray if b == handler.chosen_items['backpack'] else color.black
        intermission_console.print(51, y_offset+1, string=f"> {b.name}" if handler.inventory_items['backpack'].index(b) == handler.current_index['backpack'] else f"{b.name}",
        bg = bg_color)
        y_offset += 1

    y_offset += 2

    intermission_console.print(51, y_offset, string="S - Shield")
    for s in handler.inventory_items['shield']:
        if s in handler.items_to_drop['shield']:
            bg_color = color.red
        else:
            bg_color = color.dark_gray if s == handler.chosen_items['shield'] else color.black
        intermission_console.print(51, y_offset+1, string=f"> {s.name}" if handler.inventory_items['shield'].index(s) == handler.current_index['shield'] else f"{s.name}",
        bg = bg_color)
        y_offset += 1

    intermission_console.print(1, 21, string="Press Enter to proceed to the next level once your choices are made...")

    # we normally see something like the below line:
    # intermission_console.blit(dest = root_console, dest_x = 0, dest_y = 0, width = 59, height = 20)
    # but we're printing directly to the root console here