from .combatant import Combatant

from input_handlers.endgame_event_handler import EndgameEventHandler

# Player - the player character, moved by the player, etc.
class Player(Combatant):

    def __init__(self, **kwargs):
        super().__init__(name = "Player", blocks_movement = True, **kwargs)

    @property
    def hp(self) -> int:
        return self._hp

    @property
    def is_alive(self) -> bool:
        return self._hp > 0

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp <= 0:
            self.engine.event_handler = EndgameEventHandler(self.engine)
            self.die()

    def die(self) -> None:
        print("You died!")