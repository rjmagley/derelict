import tcod

from entities.player import Player
from input_handlers.game_event_handler import GameEventHandler
from actions.actions import *
from game_engine import GameEngine
from floor_generation import generate_floor, generate_test_floor2

def main():
    screen_width = 80
    screen_height = 24

    player = Player(x=40, y=12, char='@', hp=10, defense=5, power=5)
    engine = GameEngine(player=player)

    map = generate_test_floor2(160, 20, engine)
    # map = generate_test_floor(160, 20, engine)
    player.map = map
    player.engine = engine

    engine.map = map

    engine.update_fov()

    tileset = tcod.tileset.load_tilesheet("tileset.png", 16, 16, tcod.tileset.CHARMAP_CP437)

    with tcod.context.new_terminal(screen_width, screen_height, tileset=tileset, title="test", vsync=False) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)
            engine.event_handler.handle_events()


if __name__ == "__main__":
    main()