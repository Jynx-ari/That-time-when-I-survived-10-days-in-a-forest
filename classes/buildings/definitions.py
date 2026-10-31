from dataclasses import dataclass

from ..aboutplayer.item_types import BuildingCategory, PlacementType

@dataclass(frozen=True)
class BuildingDefinition:
    name :str
    category : BuildingCategory
    cost : dict[str, int]
    max_health : int

    placement_type: PlacementType = PlacementType.GROUND

    damage : float = 0.0
    attack_range : float = 0.0
    fire_interval : float = 0.0
    stun_dur : float = 0.0