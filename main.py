import tcod

from entities.player import Player
from actions.actions import *
from game_engine import GameEngine
from floor_generation import generate_floor, generate_test_floor2

def main():
    screen_width = 80
    screen_height = 24

    tileset = tcod.tileset.load_tilesheet("tileset.png", 16, 16, tcod.tileset.CHARMAP_CP437)

    context = tcod.context.new(columns=screen_width, rows=screen_height, tileset=tileset, title="Derelict", vsync=False)

    context.renderer = 5
        
    print(context.sdl_renderer)

    root_console = tcod.console.Console(screen_width, screen_height, order="F")
    player = Player(x=40, y=12, char='@', hp=10, defense=5, power=5)
    engine = GameEngine(player=player, root_console=root_console, context=context)

    map = generate_test_floor2(160, 20, engine)
    # map = generate_test_floor(160, 20, engine)
    player.map = map
    player.engine = engine

    engine.change_map(map)
    engine.message_log.add_message("hai2u")

    engine.update_fov()

    while True:
        engine.render()
        engine.event_handler.handle_events()


if __name__ == "__main__":
    main()