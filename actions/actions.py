from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Tuple

from entities.combatant import Combatant

if TYPE_CHECKING:
    from game_engine import GameEngine
    from entities import BaseEntity
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
    def direction(self) -> Tuple[int, int]:
        return self.dx, self.dy

    @property
    def destination(self) -> Tuple[int, int]:
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[BaseEntity]:
        return self.engine.map.get_blocking_entity_at_location(*self.destination)

    @property
    def target_entity(self) -> Optional[BaseEntity]:
        for e in self.engine.map.get_entities_at_location(*self.destination):
            if isinstance(e, Combatant) and e.is_alive:
                return e

        return None

    def perform(self) -> None:
        raise NotImplementedError()


class BumpAction(DirectionalAction):
    def perform(self) -> None:
        if isinstance(self.blocking_entity, Combatant) and self.blocking_entity.is_alive:
            return MeleeAction(self.entity, *self.direction).perform()
        else:
            return MovementAction(self.entity, *self.direction).perform()


class MovementAction(DirectionalAction):

    def perform(self) -> None:
        destination_x = self.entity.x + self.dx
        destination_y = self.entity.y + self.dy

        if not self.engine.map.in_bounds(*self.destination):
            return
        if not self.engine.map.tiles['walkable'][*self.destination]:
            return
        if self.engine.map.get_blocking_entity_at_location(*self.destination):
            return

        self.entity.move(*self.direction)

class MeleeAction(DirectionalAction):
    
    def perform(self) -> None:

        target = self.target_entity
        print(f"{self.entity.name} attempts to attack {target.name}")
        if not target:
            return

        self.entity.attack(target)

class WaitAction(Action):
    def perform(self) -> None:
        pass