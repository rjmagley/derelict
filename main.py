import tcod

from entities.starting_player_creator import generate_player
from actions.actions import *
from game_engine import GameEngine
from items.weapon_generator import place_random_common_weapon
from floor_generation.floor_generation import generate_floor, generate_test_floor2

from entities.modifiers import Modifier, ModifierProperty

from powers.smite import SmitePower

from input_handlers.intro_handler import IntroEventHandler

def main():
    screen_width = 80
    screen_height = 24

    tileset = tcod.tileset.load_tilesheet("tileset.png", 16, 16, tcod.tileset.CHARMAP_CP437)

    context = tcod.context.new(columns=screen_width, rows=screen_height, tileset=tileset, title="Derelict", vsync=False)

    root_console = tcod.console.Console(screen_width, screen_height, order="F")

    # start of game - present player start options
    # this is hacky for right now - will be improved later
    

    context.present(root_console)

    selected = None

    continue_to_game = False
    intro_handler = IntroEventHandler()
    while continue_to_game == False:
        print("continuing")
        root_console.print(1, 1, string="Welcome to Derelict", fg=color.white)
        root_console.print(1, 2, string="Select your class with a letter key:", fg=color.white)

        root_console.print(1, 4, string="a. Noble", fg=color.white)
        root_console.print(1, 5, string="b. Bulwark", fg=color.white)
        root_console.print(1, 6, string="c. Ranger", fg=color.white)
        key = intro_handler.handle_events()
        print(key)
        match key:
            
            case tcod.event.KeySym.a:
                selected = 'noble'

            case tcod.event.KeySym.b:
                selected = 'bulwark'

            case tcod.event.KeySym.c:
                selected = 'ranger'

            case tcod.event.KeySym.d:
                selected = 'test'

            case tcod.event.KeySym.RETURN:
                if selected != None:
                    continue_to_game = True

        match selected:
            case 'noble':
                root_console.print(1, 8, string="Noble", fg=color.white)
                root_console.print(1, 9, string="The Noble is a skilled psychic, and familiar with pistols, submachine \nguns, rifles and melee weapons.", fg=color.white)
                root_console.print(1, 12, string="You will start with a heavy pistol, a longsword, a light rifle\nand a few psychic abilities.", fg=color.white)
            case 'bulwark':
                root_console.print(1, 8, string="Bulwark", fg=color.white)
                root_console.print(1, 9, string="The Bulwark is a powerful ranged combatant, albeit with weaker \npsychic potential. Your skill with arms is increased, however.", fg=color.white)
                root_console.print(1, 12, string="You will start with a heavy rifle, a shotgun, a shoulder-mount\n laser, and minimal psychic training.", fg=color.white)
            case 'ranger':
                root_console.print(1, 8, string="Ranger", fg=color.white)
                root_console.print(1, 9, string="The Ranger is skilled at distance combat, with small arms or psychic\npowers - although your heavier weapons are lacking.", fg=color.white)
                root_console.print(1, 12, string="You will start with a sniper rifle, a heavy pistol, an axe,\n and a few useful utility powers.", fg=color.white)
            case 'test':
                root_console.print(1, 8, string="Test", fg=color.white)
                root_console.print(1, 9, string="I'm here to test stuff!", fg=color.white)
                root_console.print(1, 12, string="You will start with... whatever needs testing!", fg=color.white)

        if selected != None:
            root_console.print(1, 15, string="Press Enter to begin.", fg=color.white)

        context.present(root_console)
        root_console.clear()

    player = generate_player(selected)
    # testing modifiers
    # player.modifiers.append(
    #     Modifier(ModifierProperty.MOVEMENT_SPEED, -8, 100, False, "Speed", color.bright_cyan, color.bright_yellow)
    # )
    player.delay = 0
    
    
    engine = GameEngine(player=player, root_console=root_console, context=context)


    
    map = generate_test_floor2(160, 20, engine)
    # map = generate_test_floor(160, 20, engine)
    player.map = map
    player.engine = engine
    player.right_hand.engine = engine
    # starting_weapon.map = map
    # starting_weapon.engine = engine

    player.powers.append(SmitePower(caster = player))
    # player.powers.append(BasePower(caster = player, power_cost = 99, name = "impossible"))

    engine.change_map(map)
    engine.message_log.add_message("hai2u")

    engine.update_fov()

    while True:
        engine.game_loop()


if __name__ == "__main__":
    main()