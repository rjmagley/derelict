from enum import auto, Enum

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