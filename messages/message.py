from typing import List, Reversible, Tuple

import textwrap

import tcod
import color

class Message():
    
    def __init__(self, text: str, fg: Tuple[int, int, int]):
        self.plain_text = text
        self.fg = fg