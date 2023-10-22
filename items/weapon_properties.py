from dataclasses import dataclass
from typing import Dict, Callable
from .base_weapon import BaseWeapon

@dataclass
class WeaponProperty():
    name: str
    description: str
    attributes_to_modify: Dict[str, int | Callable | float]

    # right now this assumes we want to either add or multiply based on the
    # property - we may want to add some extra data to this dictionary
    # to determine which operation to perform
    def modify_weapon(self, weapon: BaseWeapon) -> None:
        for k, v in self.attributes_to_modify.items():
            if k in ['reload_time', 'optimal_range', 'damage_die']:
                setattr(weapon, k, getattr(weapon, k) + v)
            elif k in ['ammunition_size', 'magazine_size']:
                setattr(weapon, k, round(getattr(weapon, k) + v))
        pass

property_cqb = WeaponProperty("CQB Optimized",
"Optimized for close-range fights. Quicker reloads,\nbut reduced optimal range.",
{
    'reload_time': -2,
    'optimal_range': -2,
    'damage_die': -1
})

property_heavy_caliber = WeaponProperty("Heavy Caliber",
"This weapon's bored for a larger caliber. Increased\ndamage, but reduced magazine size and reduced ammo efficiency.",
{
    'damage_die': 1,
    'ammunition_size': 1.2,
    'magazine_size': 0.7
})