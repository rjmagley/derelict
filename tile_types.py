from typing import Tuple

import color
import numpy  # type: ignore

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = numpy.dtype(
    [
        ("char", int),  # Unicode codepoint.
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = numpy.dtype(
    [
        ("walkable", numpy.bool_),  # True if this tile can be walked over.
        ("blocking", numpy.bool_),  # True if this tile is solid/blocks fire.
        ("transparent", numpy.bool_),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
        ("light", graphic_dt) # Graphics for when this tile is in FOV
    ]
)


def new_tile(
    *,
    walkable: int,
    blocking: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]
) -> numpy.ndarray:
    """Helper function for defining individual tile types """
    return numpy.array((walkable, blocking, transparent, dark, light), dtype=tile_dt)

unseen = numpy.array((ord(" "), color.white, color.black), dtype=graphic_dt)

floor = new_tile(
    walkable=True,
    blocking=False,
    transparent=True,
    dark=(ord('·'), color.dark_gray, color.black),
    light=(ord('·'), color.light_gray, color.black),
)

wall = new_tile(
    walkable=False,
    blocking=True,
    transparent=False,
    dark=(ord('#'), color.dark_gray, color.black),
    light=(ord('#'), color.white, color.black),
)

transparent_wall = new_tile(
    walkable=False,
    blocking=True,
    transparent=True,
    dark=(ord('▓'), color.dark_gray, color.black),
    light=(ord('▓'), color.bright_blue, color.black),
)

chasm = new_tile(
    walkable=False,
    blocking=False,
    transparent=True,
    dark=(ord(' '), color.black, color.black),
    light=(ord(' '), color.black, color.black),
)

down_stairs = new_tile(
    walkable=True,
    blocking=False,
    transparent=True,
    dark=(ord('>'), color.dark_gray, color.black),
    light=(ord('>'), color.white, color.black),
)