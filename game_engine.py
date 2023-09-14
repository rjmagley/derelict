from typing import Set, Iterable, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from entities.base_entity import BaseEntity
    from floor_map import FloorMap

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

    map: FloorMap

    def __init__(self, player: Player):
        self.event_handler = EventHandler(self)
        self.player = player

    def handle_enemy_actions(self) -> None:
        for e in self.map.entities - {self.player}:
            if e.ai:
                e.ai.perform()

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