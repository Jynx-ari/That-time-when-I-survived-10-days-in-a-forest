from dataclasses import dataclass

from .item_types import BuildingCategory

@dataclass(frozen=True)
class BuildingDefinition:
    name :str
    category : BuildingCategory
    cost : dict[str, int]
    max_health : int
    damage : float = 0.0
    attack_range : foat = 0.0
    fire_interval : float = 0.0
    stun_dur : float = 0.0