from dataclasses import dataclass

from .item_types import (
    AmmoType,
    DamageType,
    EquipmentSlot,
    WeaponType,
    ConsumableType,
)
T = True
@dataclass(frozen=T)
class WeaponProperties:
    damage : float
    weapon_type : WeaponType
    ammo_type: AmmoType | None = None
    pellet_count : int = 1
    fire_interval : float=0.0
    damage_type : DamageType = DamageType.PHYSICAL

@dataclass(frozen=T)
class AmmoProperties:
    ammo_type : AmmoType

@dataclass(frozen=T)
class HealingProperties:
    heal_amount: int

@dataclass(frozen=T)
class EquipmentProperties:
    slot : EquipmentSlot

@dataclass(frozen=T)
class MaterialProperties:
    tags : frozenset[str] #i wonder what is frozenset does??

@dataclass(frozen=T)
class DeployableProperties:
    building_id : str

@dataclass(frozen=T)
class ConsumableProperties:
    consumable_type: ConsumableType
    effect_value: float = 0.0 #future implementation
    duration: float = 0.0 