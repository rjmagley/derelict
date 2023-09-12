from .combatant import Combatant

# Player - the player character, moved by the player, etc.
class Player(Combatant):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)