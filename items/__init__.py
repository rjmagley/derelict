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

class AmmunitionType(StrEnum):
    LIGHT = "light"
    HEAVY = "heavy"
    EXPLOSIVE = "explosive"
    EXOTIC = "exotic"
    