from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from game_engine import GameEngine
    from entities.base_entity import BaseEntity
    from entities.combatant import Combatant
    from entities.mover import Mover

class Action():

    def __init__(self, entity: BaseEntity) -> None:
        self.entity = entity

    @property
    def engine(self) -> GameEngine:
        return self.entity.map.engine

    def perform(self) -> None:
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()

class DirectionalAction(Action):
    def __init__(self, entity: BaseEntity, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def blocking_entity(self) -> Optional[BaseEntity]:
        return self.engine.map.get_blocking_entity_at_location(self.dx, self.dy)

    def perform(self) -> None:
        raise NotImplementedError()


class BumpAction(DirectionalAction):
    def perform(self) -> None:
        if self.blocking_entity:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()


class MovementAction(DirectionalAction):

    def perform(self) -> None:
        destination_x = self.entity.x + self.dx
        destination_y = self.entity.y + self.dy

        if not self.engine.map.in_bounds(destination_x, destination_y):
            return
        if not self.engine.map.tiles['walkable'][destination_x, destination_y]:
            return
        if self.engine.map.get_blocking_entity_at_location(destination_x, destination_y):
            return

        self.entity.move(self.dx, self.dy)

class MeleeAction(DirectionalAction):
    
    def perform(self) -> None:

        target = self.blocking_entity
        
        if not target:
            return
        print("attacking {target.name}")

class WaitAction(Action):
    def perform(self) -> None:
        pass