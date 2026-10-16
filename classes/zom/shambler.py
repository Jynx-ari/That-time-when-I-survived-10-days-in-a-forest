from .zombie import Zombie

default_config = {
    "health": 100,
    "speed": 60,
    "damage_to_towers": 10,
    "damage_to_player": 0.4,
}

class Shambler(Zombie):
    def __init__(self, pos):
        super().__init__(
            pos,
            health=default_config["health"],
            speed=default_config["speed"],
            damage_to_towers=default_config["damage_to_towers"],
            damage_to_player=default_config["damage_to_player"]
        )
        
