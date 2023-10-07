from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from string import ascii_uppercase

from . import ESCAPE_KEYS

import tcod

from actions.actions import Action

from .event_handler import EventHandler

if TYPE_CHECKING:
    from game_engine import GameEngine
    from . import game_event_handler
    from . import view_item_event_handler
    



from input_handlers.handler_types import HandlerType

class PowerListHandler(EventHandler):

    def __init__(self, engine: GameEngine):
        super().__init__(engine)
        self.handler_type = HandlerType.POWER_LIST
        self.power_list = engine.player.powers

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        key = event.sym

        power_keys = ascii_uppercase[0:len(self.power_list)]
        powers = {k: i for k, i in zip(power_keys, self.power_list)}

        # if key.label in power_keys:
        #     self.engine.switch_handler(HandlerType.ITEM_VIEW, item=inventory_items[key.label])

        if key in ESCAPE_KEYS:
            self.engine.switch_handler(HandlerType.GAME)