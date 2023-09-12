import tcod

from entities.player import Player
from entities.combatant import Combatant
from input_handlers.event_handler import EventHandler
from actions.actions import *
from game_engine import GameEngine
from floor_generation import generate_floor

def main():
    screen_width = 80
    screen_height = 24

    player = Player(x=40, y=12, char='@')
    npc = Combatant(x=30, y=6)
    entities={player, npc}

    map = generate_floor(80, 20, player)

    event_handler = EventHandler()

    engine = GameEngine(event_handler=event_handler, player=player, map=map)  

    tileset = tcod.tileset.load_tilesheet("tileset.png", 16, 16, tcod.tileset.CHARMAP_CP437)

    with tcod.context.new_terminal(screen_width, screen_height, tileset=tileset, title="test", vsync=False) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)

            events = tcod.event.wait()

            engine.handle_events(events)


if __name__ == "__main__":
    main()