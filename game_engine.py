from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from actions.actions import EscapeAction, MovementAction
from entities.base_entity import BaseEntity
from entities.player import Player
from input_handlers.event_handler import EventHandler
from floor_map import FloorMap


# GameEngine - responsible for holding state of entire game - entities, maps,
# and so on, as well as drawing to console
class GameEngine():
    def __init__(self, event_handler: EventHandler, player: Player, map: FloorMap):
        self.event_handler = event_handler
        self.player = player
        self.map = map
        self.update_fov()

    def handle_events(self, events: Iterable[Any]) -> None:
        for e in events:
            action = self.event_handler.dispatch(e)

            if action is None:
                continue

            if isinstance(action, MovementAction):
                if self.map.tiles['walkable'][self.player.x + action.dx, self.player.y + action.dy]:
                    self.player.move(dx=action.dx, dy=action.dy)

            elif isinstance(action, EscapeAction):
                raise SystemExit

        self.update_fov()

    def render(self, console: Console, context: Context) -> None:
        self.map.render(console)

        context.present(console)

        console.clear()

    def update_fov(self) -> None:
        self.map.visible[:] = compute_fov(
            self.map.tiles['transparent'],
            (self.player.x, self.player.y),
            radius=8
        )

        self.map.explored |= self.map.visible