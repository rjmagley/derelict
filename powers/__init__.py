from __future__ import annotations

from enum import StrEnum

class PowerSkill(StrEnum):
    OFFENSE = "offensive"
    DEFENSE = "defensive"
    MANIPULATION = "manipulative"
    ENHANCE = "enhancement"

# these tags determine various aspects of powers - at the time of writing this,
# it's primarily about how it's targeted, but other things could end up in here
class PowerTags(StrEnum):
    ENEMY_TARGET = "targets enemy"
    FREE_TARGET = "can target anywhere"
    SELF_TARGET = "targets player"