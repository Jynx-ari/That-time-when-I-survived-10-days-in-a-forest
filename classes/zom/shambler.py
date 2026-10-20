from .zombie import Zombie

default_config = {
    "health": 100,
    "speed": 60,
    "damage_to_tower": 10,
    "damage_to_player": 4,
}

class Shambler(Zombie):
    def __init__(self, pos):
        super().__init__(
            pos,
            health=default_config["health"],
            speed=default_config["speed"],
            damage_to_tower=default_config["damage_to_tower"],
            damage_to_player=default_config["damage_to_player"]
        )
        
