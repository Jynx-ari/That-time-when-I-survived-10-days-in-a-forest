from .zombie import Zombie

default_config = {
    "health": 100,
    "speed": 60,
    "damage_to_tower": 8,
    "damage_to_player": 2.35, #base 4
    "attack cooldown": 0,
    "attack interval": 1.2
}

class Shambler(Zombie):
    def __init__(self, pos):
        super().__init__(
            pos,
            health=default_config["health"],
            speed=default_config["speed"],
            damage_to_tower=default_config["damage_to_tower"],
            damage_to_player=default_config["damage_to_player"],
            attack_cd=0.0,
            attack_interval=default_config["attack interval"]
        )
        
