from .zombie import Zombie

default_config = {
    "health": 100,
    "speed": 1.0,
    "damage_to_towers": 10,
    "damage_to_player": 0.4,
}

class Shambler(Zombie):
    def __init__(self, pos):
        super().__init__(
            pos,
            health=100,
            speed=60
        )
        
