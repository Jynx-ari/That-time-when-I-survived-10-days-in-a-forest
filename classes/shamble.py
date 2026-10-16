from classes.zombie import Zombie

default_config = {
    "health": 100,
    "speed": 1.0,
    "damage_to_towers": 10,
    "damage_to_player": 0.4,
}

class Shamble(Zombie):
    def __init__(self):
        super().__init__()
        
