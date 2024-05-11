from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tcod.console import Console
    from entities.player import Player

def render_endgame_status(root_console: 'Console', center_console: 'Console', player: 'Player') -> None:
    center_console.print(1, 1, string="You died...")
    center_console.print(1, 2, string="Some day actual information will be here.")
    center_console.print(1, 3, string="Hit Escape to exit.")

    center_console.blit(dest = root_console, dest_x = 0, dest_y = 0, width = 60, height = 20)
    center_console.clear()