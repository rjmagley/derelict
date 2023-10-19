import tcod

MOVE_KEYS = {
    # Arrow keys.
    tcod.event.KeySym.UP: (0, -1),
    tcod.event.KeySym.DOWN: (0, 1),
    tcod.event.KeySym.LEFT: (-1, 0),
    tcod.event.KeySym.RIGHT: (1, 0),
    # Numpad keys.
    tcod.event.KeySym.KP_1: (-1, 1),
    tcod.event.KeySym.KP_2: (0, 1),
    tcod.event.KeySym.KP_3: (1, 1),
    tcod.event.KeySym.KP_4: (-1, 0),
    tcod.event.KeySym.KP_6: (1, 0),
    tcod.event.KeySym.KP_7: (-1, -1),
    tcod.event.KeySym.KP_8: (0, -1),
    tcod.event.KeySym.KP_9: (1, -1),
    # Vi keys.
    tcod.event.KeySym.h: (-1, 0),
    tcod.event.KeySym.j: (0, 1),
    tcod.event.KeySym.k: (0, -1),
    tcod.event.KeySym.l: (1, 0),
    tcod.event.KeySym.y: (-1, -1),
    tcod.event.KeySym.u: (1, -1),
    tcod.event.KeySym.b: (-1, 1),
    tcod.event.KeySym.n: (1, 1),
}

WAIT_KEYS = {
    tcod.event.KeySym.KP_5,
    tcod.event.KeySym.CLEAR,
    tcod.event.KeySym.PERIOD
}

CURSOR_Y_KEYS = {
    tcod.event.KeySym.UP: -1,
    tcod.event.KeySym.DOWN: 1,
}

CONFIRM_KEYS = {
    tcod.event.KeySym.RETURN,
    tcod.event.KeySym.KP_ENTER
}

ESCAPE_KEYS = {
    tcod.event.KeySym.ESCAPE
}

from typing import Set, Iterable, Any, TYPE_CHECKING, Tuple

from .event_handler import EventHandler
from .endgame_event_handler import EndgameEventHandler
from .game_event_handler import GameEventHandler
from .inventory_view_event_handler import InventoryViewEventHandler
from .look_event_handler import LookEventHandler
from .message_history_handler import MessageHistoryHandler
from .view_item_event_handler import ViewItemEventHandler
from .targeting_handler import TargetingEventHandler
from .character_profile_handler import CharacterProfileEventHandler
from .power_list_handler import PowerListHandler
from .handler_types import HandlerType
from .power_targeting_handler import PowerTargetingEventHandler
from .weapon_select_handler import WeaponSelectEventHandler

def provide_handler(handler: HandlerType) -> type[EventHandler]:
    match handler:
        case HandlerType.ENDGAME:
            return EndgameEventHandler
        case HandlerType.GAME:
            return GameEventHandler
        case HandlerType.INVENTORY_VIEW:
            return InventoryViewEventHandler
        case HandlerType.ITEM_VIEW:
            return ViewItemEventHandler
        case HandlerType.LOOK:
            return LookEventHandler
        case HandlerType.MESSAGE_HISTORY:
            return MessageHistoryHandler
        case HandlerType.TARGETING:
            return TargetingEventHandler
        case HandlerType.CHARACTER_PROFILE:
            return CharacterProfileEventHandler
        case HandlerType.POWER_LIST:
            return PowerListHandler
        case HandlerType.POWER_TARGETING:
            return PowerTargetingEventHandler
        case HandlerType.WEAPON_SELECT:
            return WeaponSelectEventHandler
