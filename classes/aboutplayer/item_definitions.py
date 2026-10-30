from dataclasses import dataclass

@dataclass(frozen=True)
class ItemDefinition: #frozen!!!
    name: str
    category: str
    color:str
    max_stack: int = 1
    heal_amount: int = 0
    damage_amount: float = 0.0
    ammo_type: str | None = None
    pellet_count: int = 1
    fire_interval: float = 0.0