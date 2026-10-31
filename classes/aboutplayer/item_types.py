from enum import Enum #im obsessed with Enums

class ItemCategory(Enum):
    WEAPON = "weapon"
    AMMO = "ammo"
    CONSUMABLE = "consumable"
    MATERIAL = "material"
    EQUIPMENT = "equipment"
    DEPLOYABLE = "deployable"

class ItemRarity(Enum): #Yes.
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"

class AmmoType(Enum):
    N9MM = "9mm"
    T12_GAUGE = "12gauge"

class WeaponType(Enum):
    PISTOL = "pistol"
    SHOTGUN = "shotgun"
    RIFLE ="rifle"
    MELEE = "melee"
    SMG = "smg"
    LAUNCHER = "launcher"
    FLAMETHROWER = "flamethrower"
    PROJECTILE = "projectile"
    BEAM = "beam" #sounds impossible to implement idk
    #this one is special:
    THROWABLE = "throwable"

class DamageType(Enum):
    PHYSICAL = "physical"
    EXPLOSIVE = "explosive"
    FIRE = "fire"
    ELECTRICAL = "electrical"#?

class EquipmentSlot(Enum):
    HELMET = "helmet"
    ARMOR = "armor"
    BACKPACK = "backpack" #?
    ACCESSORY = "accessory"

class BuildingCategory(Enum):
    DEFENSE = "defense"
    UTILITY = "utility"
    TRAP = "trap"

class PlacementType(Enum):
    GROUND = "ground"
    WALL = "wall"
    UNRESTRICTED = "unrestricted"

class ConsumableType(Enum):
    HEALING = "healing"
    REPAIR = "repair"
    BOOST = "boost"