from __future__ import annotations

from enum import auto, StrEnum

class WeaponType(StrEnum):
    PISTOL = "pistol"
    RIFLE = "rifle"
    SMG = "smg"
    SHOTGUN = "shotgun"
    LAUNCHER = "launcher"
    HEAVY = "heavy"
    ENERGY = "energy"
    SWORD = "sword"
    AXE = "axe"
    POLEARM = "polearm"
    BLUNT = "blunt"
    SHIELD = "shield"

class ArmorType(StrEnum):
    HELMET = "helmet"
    CHEST = "chestplate"
    ARMS = "arms"
    LEGS = "legs"
    BACKPACK = "backpack"
    SHIELD_GENERATOR = "shield"
    MAGAZINE = "magazine"

class AmmunitionType(StrEnum):
    LIGHT = "light"
    HEAVY = "heavy"
    EXPLOSIVE = "explosive"
    EXOTIC = "exotic"
    ENERGY = "energy"
    # energy is a special case - will draw from player's suit

# standard - standard magazine reload
# single - reload one round at a time - tube magazines, grenade launchers
# belt - pulls directly from player's ammunition
# recharge - no reload, uses suit energy
class ReloadType(StrEnum):
    STANDARD = "standard"
    SINGLE = "single"
    BELT = "belt"
    RECHARGE = "recharge"

# various properties that armor can have, positive or negative
# I wonder if it would make sense for these to also be properties attached to
# various buffs, status effects, etc.
# that might be a unification for later though
class ArmorProperty(StrEnum):
    ENERGY_CAPACITY = "energy capacity"
    ENERGY_REGENERATION = "energy regeneration"
    BASE_ARMOR = "base armor"
    BASE_SHIELD = "base shield"
    SHIELD_REBOOT_TIME = "shield reboot time"
    SHIELD_REGENERATION = "shield regeneration"
    DAMAGE_RESISTANCE = "damage resistance"
    BASE_PSY = "base psy"
    VISION_RANGE = "vision range"

class RangedWeaponProperty(StrEnum):
    SAMPLE = "sample"

# do I need these weapon enums? they're currently used by the random weapon
# selector/generator
# we'll just go with them for now, I have a feeling they aren't necessary
class WeaponName(StrEnum):
    # common weapons start here
    BURST_PISTOL = "burst pistol"
    LIGHT_SMG = "light smg"
    HEAVY_REPEATER = "heavy repeater"
    SHOTGUN = "shotgun"
    HEAVY_AUTOGUN = "heavy autogun"
    LIGHT_AUTOCANNON = "light autocannon"
    ENERGY_RIFLE = "energy rifle"
    LONGSWORD = "long sword"
    # rare weapons start here

    MEDIUM_IRON = "Medium Iron"
    HOLD_THAT_THOUGHT = "Hold That Thought"

    # exotic weapons start here
    THIRD_RAIL = "The Third Rail"

class ArmorName(StrEnum):
    # rare armor start here
    # there's no common armor before this because the player starts with the
    # common armor they need - no more is randomly generated
    TS_ONE = "Truesight One Monocular"