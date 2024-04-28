from enum import auto, Enum

# defining HandlerTypes so that handlers know what they are -
# makes it a little easier to switch handlers when necessary
class HandlerType(Enum):
    ENDGAME = auto()
    GAME = auto()
    INVENTORY_VIEW = auto()
    ITEM_VIEW = auto()
    LOOK = auto()
    MESSAGE_HISTORY = auto()
    TARGETING = auto()
    CHARACTER_PROFILE = auto()
    POWER_LIST = auto()
    POWER_TARGETING = auto()
    WEAPON_SELECT = auto()
    INTERMISSION = auto()