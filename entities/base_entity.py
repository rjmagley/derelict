from typing import TYPE_CHECKING, Tuple
import color


# BaseEntity - the most basic entity class
# basically, anything that isn't a map tile - players, enemies, items, etc.
class BaseEntity():

    # char can be a single character, or a Unicode code point
    # https://python-tcod.readthedocs.io/en/latest/tcod/charmap-reference.html#code-page-437 for reference
    def __init__(self, x: int, y: int, char: str=chr(0x2022), color: Tuple[int, int, int] = color.white, name: str="<unnamed>", blocks_movement: bool=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
