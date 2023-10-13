from typing import List, Reversible, Tuple, Generator, Iterable

from .message import Message

import textwrap

import tcod
import color

class MessageLog:

    def __init__(self) -> None:
        self.messages: List[Message] = []

    def add_message(self, text: str, fg: Tuple[int, int, int] = color.white) -> None:
        self.messages.append(Message(text, fg))
        if len(self.messages) > 200:
            self.messages.pop(0)

    def return_messages(self) -> Iterable[tuple[str, Tuple[int, int, int]]]:
        for m in reversed(self.messages):
            for l in reversed(textwrap.wrap(m.plain_text, 80)):
                yield l, m.fg

    def return_last_message(self) -> Tuple[str, Tuple[int, int, int]]:
        if len(self.messages) >= 1:
            return (self.messages[-1].plain_text, self.messages[-1].fg)
        else:
            return ("", (0,0,0))