from __future__ import annotations

from . import MOVE_KEYS, WAIT_KEYS, CURSOR_Y_KEYS, CONFIRM_KEYS, ESCAPE_KEYS

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions import ActionResult
from actions.actions import Action, EscapeAction, BumpAction, WaitAction, PickupItemAction, PlayerReloadAction

if TYPE_CHECKING:
    from game_engine import GameEngine

from .event_handler import EventHandler

from input_handlers.handler_types import HandlerType
from items.ranged_weapon import RangedWeapon
from items.ranged_energy_weapon import RangedEnergyWeapon

class WeaponSelectEventHandler(EventHandler):

    def __init__(self, engine: GameEngine):
        super().__init__(engine)
        self.handler_type = HandlerType.WEAPON_SELECT
        self.weapons = [w for w in engine.player.equipped_weapons if w != None]
        self.weapon_keys = ['1', '2', '3', '4']
        self.weapon_dict = {k: w for k, w in zip(self.weapon_keys[0:len(self.weapons)], self.weapons)}

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        key = event.sym


        if key.label in self.weapon_keys:
            self.engine.switch_handler(HandlerType.TARGETING, weapon=self.weapon_dict[key.label])

        if key in ESCAPE_KEYS:
            self.engine.switch_handler(HandlerType.GAME)