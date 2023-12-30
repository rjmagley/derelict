from __future__ import annotations

from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING, List

from .combatant import Combatant
from items.base_weapon import BaseWeapon
from items.ranged_weapon import RangedWeapon
from items.melee_weapon import MeleeWeapon
from items.ranged_recharge_weapon import RangedRechargeWeapon

from actions import ActionResult

from .pickups.ammo_pickup import AmmoPickup
from .pickups import PickupType

from die_rollers import standard_roll_target, enemy_attack_roll
from render_order import RenderOrder
import color

import random

if TYPE_CHECKING:
    from .pickups import BasePickup
    from floor_map import FloorMap

# the Enemy class represents anything that the player is expected to fight/kill
# - mobile enemies, turrets, etc.
# the Mover class can represent things that need to move and act but don't take
# damage or damage others
class Enemy(Combatant):

    map: FloorMap
    
    def __init__(self, level: int, hp: int, defense: int, weapons: List[BaseWeapon], ranged_skill: int = 12, melee_skill: int = 12, pickup_table: List[Tuple[PickupType, int]] = [], **kwargs):
        super().__init__(**kwargs)
        # 'level' is a rough evaluation of how challenging the enemy is
        #going to be used, to determine spawning, encounter difficulty, etc.
        self.level = level
        self.hp = hp
        self.defense = defense
        self.weapons = weapons
        for weapon in weapons:
            weapon.owner = self
        # I don't think I want enemies picking up weapons, at least normal ones
        # so pre-determining these lists in advance is fine
        self.ranged_weapons = [w for w in weapons if isinstance(w, RangedWeapon)]
        self.melee_weapons = [w for w in weapons if isinstance(w, MeleeWeapon)]
        # these two skill attributes will be used for ranged combat
        # rather than give enemies a whole set of skills
        self.ranged_skill = ranged_skill
        self.melee_skill = melee_skill

        self.pickup_table = pickup_table

    def ranged_attack(self, target: Combatant, weapon: RangedWeapon) -> ActionResult:
        damage = weapon.fire()
        if enemy_attack_roll(self.ranged_skill, weapon.calculate_distance_modifier(self, target)):
            message = f"The {self.name} hits the {target.name} for {damage} damage."
            target.take_damage(damage)
            return ActionResult(True, message, color.white, 10)
        else:
            return ActionResult(True, f"The {self.name} misses the {target.name}.", color.light_gray, 10)

    # melee attacks probably do not work yet
    def melee_attack(self, target: Combatant) -> ActionResult:
        damage = self.melee_weapons[0].roll_damage()
        print(f"attempting melee attack for {damage}")
        if standard_roll_target(self.melee_skill):
            message = f"The {self.name} hits the {target.name} for {damage} damage."
            target.take_damage(damage)
            return ActionResult(True, message, color.white, 10)
        else:
            return ActionResult(True, f"The {self.name} misses the {target.name}.", color.light_gray, 10)

    # needs a take damage method
    def take_damage(self, value: int) -> None:
        damage = value - self.defense
        if damage >= 0:
            self.hp -= damage
            if self.hp <= 0:
                self.engine.dying_entities.append(self)

    def periodic_refresh(self):
        super().periodic_refresh()
        for w in self.weapons:
            if isinstance(w, RangedRechargeWeapon):
                w.recharge()

    def die(self) -> None:
        # this eventually needs to become a different type of corpse-object
        # rather than just becoming a different kind of 'enemy'
        self.engine.add_message(f"The {self.name} dies!", color.red)
        self.char = "%"
        self.color = color.red
        self.blocks_movement = False
        self.ai = None
        self.name = f"remains of {self.name}"
        self.render_order = RenderOrder.CORPSE

        for p in [p for p in self.pickup_table if p != None]:
            if random.randint(0, 100) > p[1]:
                self.map.place_entity_on_map(AmmoPickup.generate_pickup(p[0], self.level + 10), self.x, self.y)
