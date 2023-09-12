from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_engine import GameEngine
    from entities.base_entity import BaseEntity

class Action():
    def perform(self, engine: GameEngine, entity: BaseEntity) -> None:
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self, engine: GameEngine, entity: BaseEntity) -> None:
        raise SystemExit()

class DirectionalAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: GameEngine, entity: BaseEntity) -> None:
        raise NotImplementedError()

class MovementAction(DirectionalAction):

    def perform(self, engine: GameEngine, entity: BaseEntity) -> None:
        print("moving")
        destination_x = entity.x + self.dx
        destination_y = entity.y + self.dy

        if not engine.map.in_bounds(destination_x, destination_y):
            return
        if not engine.map.tiles['walkable'][destination_x, destination_y]:
            return
        if engine.map.get_blocking_entity_at_location(destination_x, destination_y):
            return

        entity.move(self.dx, self.dy)