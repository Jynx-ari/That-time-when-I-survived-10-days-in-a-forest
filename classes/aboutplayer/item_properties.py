from dataclasses import dataclass

@dataclass(frozen=True)
class WeaponProperties: #so its easier to manage
    damage: float
    ammo_type: str