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