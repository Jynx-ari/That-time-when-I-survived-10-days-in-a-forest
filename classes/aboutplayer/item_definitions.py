from dataclasses import dataclass

from .item_types import ItemCategory, ItemRarity

from .item_properties import(
    WeaponProperties,
    AmmoProperties,
    HealingProperties,
    EquipmentProperties,
    MaterialProperties,
    DeployableProperties,
    ConsumableProperties,
    ToolProperties,
)

@dataclass(frozen=True)
class ItemDefinition:
    name : str
    category : ItemCategory
    color : str
    max_stack : int = 1
    rarity : ItemRarity = ItemRarity.COMMON

    weapon : WeaponProperties | None = None
    ammo : AmmoProperties | None = None
    healing : HealingProperties | None = None
    equipment : EquipmentProperties | None = None
    material : MaterialProperties | None = None
    deployable : DeployableProperties | None = None
    consumable : ConsumableProperties | None = None
    tool : ToolProperties | None = None
