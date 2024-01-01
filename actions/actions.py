from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Tuple

from decimal import Decimal

from entities.combatant import Combatant
from entities.mover import Mover
from . import ActionResult
import color
from entities.player import Player
from entities.pickups import BasePickup
from entities.pickups.ammo_pickup import AmmoPickup
from items.ranged_weapon import RangedWeapon
from items.base_item import BaseItem

if TYPE_CHECKING:
    from game_engine import GameEngine
    from entities import BaseEntity
    from entities.combatant import Combatant
    

# actions return a boolean to determine if a turn was taken or not
# the player shouldn't be penalized for attempting an impossible action

# can someone remind me why these are all classes? was it to reduce some repetition
# by using inheritance?

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
            if isinstance(e, Mover) and e.is_alive:
                return e

        return None

    def perform(self) -> None:
        raise NotImplementedError()


class BumpAction(DirectionalAction):

    def perform(self) -> ActionResult:
        if isinstance(self.blocking_entity, Combatant) and self.blocking_entity.is_alive:
            return MeleeAction(self.entity, self.blocking_entity).perform()
        else:
            if isinstance(self.entity, Player):
                return PlayerMovementAction(self.entity, *self.direction).perform()
            else:
                return MovementAction(self.entity, *self.direction).perform()

class MovementAction(DirectionalAction):

    def perform(self) -> ActionResult:
        if not self.engine.map.in_bounds(*self.destination):
            return ActionResult(False, time_taken = 10)
        if not self.engine.map.tiles['walkable'][*self.destination]:
            return ActionResult(False, time_taken = 10)
        if self.engine.map.get_blocking_entity_at_location(*self.destination):
            return ActionResult(False, time_taken = 10)

        self.entity.move(*self.direction)
        return ActionResult(True, time_taken = self.entity.move_speed)


class PlayerMovementAction(DirectionalAction):

    def perform(self) -> ActionResult:
        if not self.engine.map.in_bounds(*self.destination):
            self.engine.add_message("You can't move there.", color.light_gray)
            return ActionResult(False, "You can't move there.", color.light_gray)
        if not self.engine.map.tiles['walkable'][*self.destination]:
            return ActionResult(False, "You can't move there.", color.light_gray)
        if self.engine.map.get_blocking_entity_at_location(*self.destination):
            return ActionResult(False, "Something blocks your way.", color.light_gray)

        self.entity.move(*self.direction)
        return ActionResult(True, time_taken = self.entity.move_speed)


class MeleeAction(DirectionalAction):

    def __init__(self, entity, target) -> None:
        super().__init__(entity, target.x, target.y)
        self.entity = entity
        self.target = target


    def perform(self) -> ActionResult:

        target = self.target
        if not target:
            return ActionResult()

        return self.entity.melee_attack(target)


class PickupItemAction(Action):

    def perform(self) -> ActionResult:
        player = self.engine.player
        item = self.engine.map.get_item_at_location(self.entity.x, self.entity.y)

        # the ActionResults here should eventually have their time_taken factor
        # into the player's stats somehow - maybe like, a talent that both
        # speeds up ammo reloading and item pickup speed?

        # if isinstance(item, AmmoPickup):
        #     player.magazine.add_ammo(item)
        #     item.on_consume()
        #     return ActionResult(True, f"You put the {item.name} into your magazine.", color.light_gray, 10)

        if isinstance(item, BaseItem):
            if player.inventory.space_remaining(item):
                self.engine.map.entities.remove(item)
                player.inventory.insert_item(item)
                if isinstance(item, RangedWeapon):
                    item.owner = player

                return ActionResult(True, f"You grab the {item.name}.", color.light_gray, 10)
            else:
                return ActionResult(False, "Your inventory is full.", color.light_gray)

        else:
            return ActionResult(False, "There's nothing to pick up.", color.light_gray)


class PlayerFireAction(Action):
    def __init__(self, entity, target, weapon) -> None:
        super().__init__(entity)
        self.player = entity
        self.target = target
        self.weapon = weapon

    # for now, weapons don't overpenetrate, a burst can't hit another target,
    # etc. - will need more work
    def perform(self) -> ActionResult:
        return self.entity.ranged_attack(self.target, self.weapon)

class PlayerReloadAction(Action):

    def __init__(self, player, weapon) -> None:
        super().__init__(player)
        self.player = player
        self.weapon = weapon

    def perform(self) -> ActionResult:
        return self.weapon.reload(self.player)

class PlayerCastPowerAction(Action):
    def __init__(self, player, power, target = None, x: Optional[int] = None, y: Optional[int] = None) -> None:
        super().__init__(player)
        self.player = player
        self.power = power
        self.target = target
        self.x = x
        self.y = y

    def perform(self) -> ActionResult:
        self.power.cast(target = self.target, x = self.x, y = self.y)
        return ActionResult(True, time_taken = 10)


class WaitAction(Action):
    def perform(self) -> ActionResult:
        return ActionResult(True, time_taken = 10)