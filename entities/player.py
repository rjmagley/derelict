from __future__ import annotations

from typing import Type, List, Optional, Any, TYPE_CHECKING

from decimal import Decimal

from enum import auto, StrEnum

from random import randint

from render_order import RenderOrder
from items.base_weapon import BaseWeapon

from actions import ActionResult

from .mover import Mover
from .combatant import Combatant
from items.melee_weapon import MeleeWeapon
from items.ranged_recharge_weapon import RangedRechargeWeapon

from items import WeaponType, AmmunitionType, ArmorType, ArmorProperty

from die_rollers import player_attack_roll, standard_roll_target, roll_dice

# from input_handlers.endgame_event_handler import EndgameEventHandler

from items.inventory import Inventory
from items.magazine import Magazine
from items.base_armor import BaseArmor

import color

if TYPE_CHECKING:
    from items.ranged_weapon import RangedWeapon
    from entities.enemy import Enemy

class PlayerSkill(StrEnum):
    DUALWIELD = "dual-wielding"

# Player - the player character, moved by the player, etc.
class Player(Combatant):

    def __init__(self, **kwargs):
        
        # the player's inventory - handles things held by the player
        # things equipped by the player are different
        self.inventory = Inventory()

        # the player's magazine is where their ammo is stored/created/etc.
        self.magazine = Magazine()

        # these six represent all the player's armor
        self.helmet = BaseArmor(armor_type = ArmorType.HELMET, properties = {ArmorProperty.BASE_ARMOR: 10})
        self.chest = BaseArmor(armor_type = ArmorType.CHEST, properties = {ArmorProperty.BASE_ARMOR: 10, ArmorProperty.DAMAGE_RESISTANCE: 3})
        self.arms = BaseArmor(armor_type = ArmorType.ARMS, properties = {ArmorProperty.BASE_ARMOR: 10})
        self.legs = BaseArmor(armor_type = ArmorType.LEGS, properties = {ArmorProperty.BASE_ARMOR: 10})
        self.backpack = BaseArmor(armor_type = ArmorType.BACKPACK, properties = {ArmorProperty.BASE_ARMOR: 10, ArmorProperty.ENERGY_CAPACITY: 50, ArmorProperty.ENERGY_REGENERATION: Decimal(10.0)})
        self.shield_generator = BaseArmor(armor_type = ArmorType.SHIELD_GENERATOR, properties = {ArmorProperty.BASE_SHIELD: 10, ArmorProperty.SHIELD_REBOOT_TIME: 5, ArmorProperty.SHIELD_REGENERATION: Decimal(15.0)})


        # weapons held by the player, in hands/on shoulders
        # some weapons take up both hands - those are considered to be in the
        # "right" hand
        self.right_hand = None
        self.left_hand = None
        self.right_shoulder = None
        self.left_shoulder = None

        # ammunition is a dictionary representing the four ammunition types
        # ammunition is stored as a number from 0 to the player's max ammo
        # (starts at 1000) and rendered as a percentage on the UI
        
        self.player_stats = {
            WeaponType.PISTOL: 10,
            WeaponType.RIFLE: 10,
            WeaponType.SMG: 10,
            WeaponType.SHOTGUN: 10,
            WeaponType.LAUNCHER: 10,
            WeaponType.HEAVY: 10,
            WeaponType.ENERGY: 10,
            WeaponType.SWORD: 10,
            WeaponType.AXE: 10,
            WeaponType.POLEARM: 10,
            WeaponType.BLUNT: 10,
            WeaponType.SHIELD: 10,
            PlayerSkill.DUALWIELD: 10
        }

        self.base_psy = 5
        self.armor_points = self.max_armor
        self.energy_points = self.max_energy
        self.shield_points = self.max_shield
        self.psy_points = self.max_psy
        self.partial_energy = 0
        self.partial_shield = 0
        self.partial_psy = 0
        self.shield_reboot_time = 0

        

        self.powers = []

        self.class_name = ""

        super().__init__(name = "Player", blocks_movement = True, render_order = RenderOrder.COMBATANT, **kwargs)



    @property
    def max_armor(self) -> int:
        return sum(self.get_armor_properties(ArmorProperty.BASE_ARMOR))

    @property
    def max_energy(self) -> int:
        return sum(self.get_armor_properties(ArmorProperty.ENERGY_CAPACITY))

    @property
    def max_shield(self) -> int:
        return sum(self.get_armor_properties(ArmorProperty.BASE_SHIELD))

    # players have 5 psy to start with
    # this will need to be modified more once talents/leveling are added
    @property
    def max_psy(self) -> int:
        return sum(self.get_armor_properties(ArmorProperty.BASE_PSY)) + self.base_psy

    # this will be modified later based on armor, talents, etc.
    @property
    def vision_radius(self) -> int:
        return sum(self.get_armor_properties(ArmorProperty.VISION_RANGE)) + 40

    # armor properties are in a dictionary
    # key is an ArmorProperty, value is an int
    # this is very different from how weapon properties are handled
    # and at some point this needs to be refactored/unified so that they can
    # be treated similarly, for ease of comprehension
    def get_armor_properties(self, armor_property: ArmorProperty) -> List[int]:
        return [a.properties[armor_property] for a in self.equipped_armor if armor_property in a.properties]

    @property
    def equipped_armor(self) -> List[BaseArmor]:
        return [self.helmet, self.chest, self.arms, self.legs, self.backpack, self.shield_generator]

    @property
    def hp(self) -> int:
        return self.armor_points

    @hp.setter
    def hp(self, value: int) -> None:
        self.armor_points -= value
        if self.armor_points <= 0:
            self.die()

    @property
    def is_alive(self) -> bool:
        return self.armor_points > 0

    @property
    def barehanded(self) -> bool:
        return self.right_hand == None and self.left_hand == None

    @property
    def twohanded_weapon(self) -> bool:
        if self.right_hand == None:
            return False
        else:
            return self.right_hand.hands == 2

    @property
    def equipped_weapons(self) -> List[Optional[BaseWeapon]]:
        return [self.right_hand, self.left_hand, self.right_shoulder, self.left_shoulder]

    @property
    def defense(self) -> int:
        return sum([a.damage_resist for a in self.equipped_armor])

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy
        item_present = self.engine.map.get_item_at_location(self.x, self.y)
        if item_present:
            self.engine.message_log.add_message(f"On the ground here is: {item_present.name}.", color.light_gray)

    # the player's HP setter is a bit messier than normal - players have
    # shields, then armor, then a few states before death
    def take_damage(self, value: int) -> None:
        print(self.shield_points)
        if self.shield_points != 0:
            remaining_damage = self.take_shield_damage(value) - sum(self.get_armor_properties(ArmorProperty.DAMAGE_RESISTANCE))
        else:
            remaining_damage = value - sum(self.get_armor_properties(ArmorProperty.DAMAGE_RESISTANCE))
        print(f"receiving {value} damage, reduced to {remaining_damage}")
        if remaining_damage > 0:
            self.armor_points -= remaining_damage
            if self.armor_points <= 0:
                print("player died")
                # self.engine.switch_handler(EndgameEventHandler)
                self.die()

    # depletes shield, returns any damage left to hit armor
    # could also do some interesting stuff with this for directly targeting
    # shields on the player
    def take_shield_damage(self, value: int) -> int:
        if value >= self.shield_points:
            remaining_damage = value - self.shield_points
            self.shield_points = 0
            self.shield_reboot_time += sum(self.get_armor_properties(ArmorProperty.SHIELD_REBOOT_TIME))
            return remaining_damage
        else:
            self.shield_points -= value
            return 0

    def has_equipped(self, item: BaseWeapon):
        return item is self.right_hand or item is self.left_hand

    # equipping should fail if unequipping two weapons to equip a two-handed
    # weapon would overflow the player's inventory
    # for right now, it doesn't, because I have other things to do
    def equip_right_hand(self, weapon: BaseWeapon) -> ActionResult:
        # store the old weapons
        if self.twohanded_weapon:
            old_weapons = [self.right_hand]
        else:
            old_weapons = [self.right_hand, self.left_hand]

        for w in old_weapons:
            self.inventory.insert_item(w)

        if weapon.hands == 1:
            self.right_hand = weapon
        else:
            self.left_hand = None
            self.right_hand = weapon
        weapon.owner = self
        self.inventory.remove_item(weapon)
        return ActionResult(True, f"You equip the {weapon.name}.", color.white, 10)

    # eventually this should probably become "equip_offhand" or something
    def equip_left_hand(self, weapon: BaseWeapon) -> ActionResult:
        if self.twohanded_weapon:
            return ActionResult(False, f"Both your hands are full.", color.light_gray)
        if weapon.hands == 1:
            self.left_hand = weapon
            weapon.owner = self
            self.inventory.remove_item(weapon)
            return ActionResult(True, f"You equip the {weapon.name} in your off hand.", color.white, 10)
        else:
            return ActionResult(False, f"The {weapon.name} is too big for your offhand.", color.light_gray)

    # all these equip actions really should be generalized to one function
    # that equips anything into any slot, maybe?
    # that's how armor will work anyways
    def equip_right_shoulder(self, weapon: BaseWeapon) -> ActionResult:
        if self.right_shoulder != None:
            self.inventory.insert_item(self.right_shoulder)
        self.inventory.remove_item(weapon)
        self.right_shoulder = weapon
        weapon.owner = self
        return ActionResult(True, f"You equip the {weapon.name} on your right shoulder.", color.white, 10)

    def equip_left_shoulder(self, weapon: BaseWeapon) -> ActionResult:
        if self.left_shoulder != None:
            self.inventory.insert_item(self.left_shoulder)
        self.inventory.remove_item(weapon)
        self.left_shoulder = weapon
        weapon.owner = self
        return ActionResult(True, f"You equip the {weapon.name} on your left shoulder.", color.white, 10)
    
    # equip_armor returns no action result because it can't happen during normal
    # gameplay - only during the intermission
    def equip_armor(self, armor: BaseArmor) -> None:
        print(f"Equipping: {armor.name}")
        # magazine is going to have to be a special case because ammo needs
        # to be transferred around - no free refills
        match armor.armor_type:
            case ArmorType.HELMET:
                self.inventory.remove_item(armor)
                self.inventory.insert_item(self.helmet)
                self.helmet = armor
            case ArmorType.CHEST:
                self.inventory.remove_item(armor)
                self.inventory.insert_item(self.chest)
                self.chest = armor
            case ArmorType.ARMS:
                self.inventory.remove_item(armor)
                self.inventory.insert_item(self.arms)
                self.arms = armor
            case ArmorType.LEGS:
                self.inventory.remove_item(armor)
                self.inventory.insert_item(self.legs)
                self.legs = armor
            case ArmorType.BACKPACK:
                self.inventory.remove_item(armor)
                self.inventory.insert_item(self.backpack)
                self.backpack = armor
            case ArmorType.SHIELD_GENERATOR:
                self.inventory.remove_item(armor)
                self.inventory.insert_item(self.shield_generator)
                self.shield_generator = armor

    def die(self) -> None:
        print("You died!")

    def ranged_attack(self, target: Combatant, weapon: RangedWeapon) -> ActionResult:
        if not weapon.is_special:
            distance_modifier = weapon.calculate_distance_modifier(self, target)
            damage = weapon.fire()
            if player_attack_roll(weapon, self, distance_modifier):
                message = f"You hit the {target.name} for {damage} damage."
                target.take_damage(damage)
                return ActionResult(True, message, color.white, weapon.fire_time)
            else:
                return ActionResult(True, f"You miss the {target.name}.", color.light_gray, weapon.fire_time)
        else:
            weapon.fire(target = target, floor = self.engine.map)
            return ActionResult(True, time_taken = weapon.fire_time)

    # no handling of dual attacks yet
    def melee_attack(self, target: Combatant) -> ActionResult:
        weapon = None
        if isinstance(self.right_hand, MeleeWeapon):
            weapon = self.right_hand
        elif isinstance(self.left_hand, MeleeWeapon):
            weapon = self.left_hand
        
        if weapon != None:
            if player_attack_roll(weapon, self):
                damage = weapon.roll_damage()
                message = f"You hit the {target.name} for {damage} damage."
                target.take_damage(damage)
                return ActionResult(True, message, color.white, 10)
            else:
                return ActionResult(True, f"You miss the {target.name}.", color.light_gray, 10)

        # barehanded attacks are very ineffective; they should be avoided
        else:
            if standard_roll_target(14):
                damage = roll_dice(2, 4)
                message = f"You hit the {target.name} with the butt of your weapon for {damage} damage."
                target.take_damage(damage)
                return ActionResult(True, message, color.white, 10)
            else:
                return ActionResult(True, f"You miss the {target.name}.", color.light_gray, 10)


    def regenerate_energy(self) -> None:
        if self.energy_points < self.max_energy:
            self.partial_energy += sum(self.get_armor_properties(ArmorProperty.ENERGY_REGENERATION))
            if self.partial_energy >= 100:
                self.partial_energy -= 100
                self.energy_points += 1
        pass

    def regenerate_shield(self) -> None:
        if self.shield_reboot_time == 0:
            if self.shield_points < self.max_shield:
                self.partial_shield += sum(self.get_armor_properties(ArmorProperty.SHIELD_REGENERATION))
                if self.partial_shield >= 100:
                    self.partial_shield -= 100
                    self.shield_points += 1
        else:
            self.shield_reboot_time -= 1
            if self.shield_reboot_time == 0:
                self.shield_points = self.max_shield // 3

    def get_energy_status(self) -> str:
        return f"{self.energy_points}/{self.max_energy}"

    def get_shield_status(self) -> str:
        return f"{self.shield_points}/{self.max_shield}"

    def get_psy_status(self) -> str:
        return f"{self.psy_points}/{self.max_psy}"

    # gonna call this every 10 auts to do things like player shield recharge,
    # ticking down status effects, etc. 
    def periodic_refresh(self):
        self.regenerate_shield()
        self.regenerate_energy()
        for w in self.equipped_weapons:
            if isinstance(w, RangedRechargeWeapon):
                w.recharge()
        pass

    # will call this when an enemy dies to the player to handle replenishing
    # psy, and other things that may need to happen
    # this has the side effect of the player regaining at most one point per
    # enemy death, with the remaining points trickling in as the player gets
    # more kills - this might need to be rolled into the periodic refresh code
    def on_enemy_death(self, enemy: Enemy):
        if self.psy_points < self.max_psy:
                self.partial_psy += randint(1, enemy.level) * 10
                if self.partial_psy >= 100:
                    self.partial_psy -= 100
                    self.psy_points += 1
        pass