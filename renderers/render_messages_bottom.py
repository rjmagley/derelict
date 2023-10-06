from __future__ import annotations

from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from messages.message_log import MessageLog
    from tcod.console import Console

def render_messages_bottom(root_console: Console, bottom_console: Console, message_log: MessageLog) -> None:
    y_offset = 3

    for message, color in message_log.return_messages():
        bottom_console.print(0, y_offset, string=message, fg=color)
        y_offset -= 1
        if y_offset < 0:
            break

    bottom_console.blit(dest = root_console, dest_x = 0, dest_y = 20, width = 80, height = 4)
    bottom_console.clear()

