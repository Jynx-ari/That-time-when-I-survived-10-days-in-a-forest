import pygame

#im starting to have a habit to make a class just for everything at this point :/

class Tower:
    def __init__(self, pos, max_health=1000):
        self.pos = pygame.Vector2(pos)

        self.max_hp = max_health
        self.curr_hp = self.max_hp
        self.display_hp = self.max_hp

        self.size = 42
    
    #Its this decorator again :0
    @property
    def is_ded_or_destroyed(self):
        return self.hp <= 0
    
    def take_damage(self, damage):
        old_hp = self.max_hp
        self.curr_hp = max(
            0,
            self.curr_hp - max(0, damage)
        )

        return old_hp - self.curr_hp