from dataclasses import dataclass
from typing import Dict, Callable
from .base_weapon import BaseWeapon
from . import ReloadType

# this may be better off as an actual class, where we just have each instance of
# it have its own modify_weapon function?
# or have each weapon have "property" slots that are just names/descriptions that
# we call a function on to overwrite/update
# this is presuming that there's no, like, way to change the properties on a
# weapon after generation
# if there is than instead of updating the weapon's stats we have to make
# them properties to calculate for every shot
# seems iffy!
# do want to rewrite this to be more wisely structured but don't want to for now
@dataclass
class WeaponProperty():
    name: str
    description: str
    attributes_to_modify: Dict[str, int | Callable | float | str]

    # right now this assumes we want to either add or multiply based on the
    # property - we may want to add some extra data to this dictionary
    # to determine which operation to perform
    def modify_weapon(self, weapon: BaseWeapon) -> None:
        for k, v in self.attributes_to_modify.items():
            if k in ['reload_time', 'optimal_range', 'damage_die',
            'accuracy_bonus', 'range_modifier']:
                setattr(weapon, k, getattr(weapon, k) + v)
            elif k in ['ammunition_size', 'magazine_size', 'fire_time']:
                setattr(weapon, k, round(getattr(weapon, k) * v))
            elif k in ['reload_type']:
                if v == 'belt':
                    weapon.reload = weapon.belt_reload
                    weapon.fire = weapon.belt_fire
                    weapon.magazine_size = 0
                    weapon.loaded_ammo = 0
                    weapon.reload_type = ReloadType.BELT
        pass

property_cqb = WeaponProperty("CQB Optimized",
"Optimized for close-range fights. Quicker reloads,\nbut reduced optimal range.",
{
    'reload_time': -2,
    'optimal_range': -2,
})

property_heavy_caliber = WeaponProperty("Heavy Caliber",
"This weapon's bored for a larger caliber. Increased\ndamage, but reduced magazine size and reduced ammo efficiency.",
{
    'damage_die': 1,
    'ammunition_size': 1.4,
    'magazine_size': 0.7
})

property_long_long_gun = WeaponProperty("Long, Long Gun",
"Extended barrel. Improved accuracy and range modifier.\nSlower fire rate.",
{
    'accuracy_bonus': 2,
    'range_interval': 2,
    'fire_time': 1.2
})

property_light_bolt = WeaponProperty("Light Bolt",
"Weapon's bolt is extremely light. Improved rate of fire.\nReduced accuracy.",
{
    'accuracy_bonus': -2,
    'fire_time': .7
})

property_belt_feeder = WeaponProperty("Belt-Feeder",
"Linked directly to your magazine - no reloading!\nAmmunition efficiency reduced.",
{
    'reload_type': 'belt',
    'ammunition_size': 1.5
})