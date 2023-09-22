from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Tuple

from entities.combatant import Combatant

import color

if TYPE_CHECKING:
    from game_engine import GameEngine
    from entities import BaseEntity
    from entities.combatant import Combatant
    from entities.mover import Mover

# actions return a boolean to determine if a turn was taken or not
# the player shouldn't be penalized for attempting an impossible action
# when actions are set up to take time to perform into account, this
# may need to change

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

    def perform(self) -> bool:
        if isinstance(self.blocking_entity, Combatant) and self.blocking_entity.is_alive:
            return MeleeAction(self.entity, *self.direction).perform()
        else:
            return MovementAction(self.entity, *self.direction).perform()


class MovementAction(DirectionalAction):

    def perform(self) -> bool:
        destination_x = self.entity.x + self.dx
        destination_y = self.entity.y + self.dy

        if not self.engine.map.in_bounds(*self.destination):
            self.engine.add_message("You can't move there.", color.light_gray)
            return False
        if not self.engine.map.tiles['walkable'][*self.destination]:
            self.engine.add_message("You can't move there.", color.light_gray)
            return False
        if self.engine.map.get_blocking_entity_at_location(*self.destination):
            return False

        self.entity.move(*self.direction)
        return True


class MeleeAction(DirectionalAction):
    
    def perform(self) -> bool:

        target = self.target_entity
        if not target:
            return False

        self.entity.attack(target)
        return True


class PickupItemAction(Action):

    def perform(self) -> bool:
        player = self.engine.player
        items = self.engine.map.get_items_at_location(self.entity.x, self.entity.y)
        if len(items) == 1:
            target_item = items[0]
            if player.inventory.space_remaining:
                self.engine.map.entities.remove(target_item)
                player.inventory.items.append(target_item)
                if player.right_hand == None:
                    player.right_hand = target_item

                self.engine.add_message(f"You grab the {target_item.name}.", color.light_gray)
                return True
            else:
                self.engine.add_message("Your inventory is full.", color.light_gray)
        else:
            self.engine.add_message("Nothing to get here.", color.light_gray)
        return False


class WaitAction(Action):
    def perform(self) -> bool:
        return True