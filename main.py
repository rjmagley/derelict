import tcod

from entities.player import Player
from actions.actions import *
from game_engine import GameEngine
from items.melee_weapon import place_random_melee_weapon
from items.ranged_weapon import get_test_belt_weapon
from items.ranged_energy_weapon import get_test_energy_weapon
from floor_generation import generate_floor, generate_test_floor2

from powers.smite import Smite

def main():
    screen_width = 80
    screen_height = 24

    tileset = tcod.tileset.load_tilesheet("tileset.png", 16, 16, tcod.tileset.CHARMAP_CP437)

    context = tcod.context.new(columns=screen_width, rows=screen_height, tileset=tileset, title="Derelict", vsync=False)

    root_console = tcod.console.Console(screen_width, screen_height, order="F")
    player = Player(x=40, y=12, char='@')
    player.delay = 0
    
    
    engine = GameEngine(player=player, root_console=root_console, context=context)


    
    map = generate_test_floor2(160, 20, engine)
    # map = generate_test_floor(160, 20, engine)
    player.map = map
    player.engine = engine
    starting_weapon = get_test_belt_weapon(40, 12, map)
    starting_weapon.owner = player
    player.inventory.items.append(starting_weapon)
    player.right_hand = starting_weapon
    # starting_weapon.map = map
    # starting_weapon.engine = engine

    player.powers.append(Smite(caster = player))
    # player.powers.append(BasePower(caster = player, power_cost = 99, name = "impossible"))

    engine.change_map(map)
    engine.message_log.add_message("hai2u")

    engine.update_fov()

    while True:
        engine.render()
        engine.handle_turns()


if __name__ == "__main__":
    main()