from __future__ import annotations

from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from messages.message_log import MessageLog
    from tcod.console import Console

def render_message_history(root_console: Console, message_log: MessageLog) -> None:
    y_offset = 23

    root_console.print(5, 0, string="Message History:")

    for message, color in message_log.return_messages():
        root_console.print(0, y_offset, string=message, fg=color)
        y_offset -= 1
        if y_offset < 2:
            break

