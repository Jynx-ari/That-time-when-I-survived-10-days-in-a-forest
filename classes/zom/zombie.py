import pygame

class Zombie():
    def __init__(self, pos, health=100, speed=0, damage_to_tower=0.0, damage_to_player=0.0):
        self.pos = pygame.Vector2(pos)
        self.health = health
        self.speed = speed
        self.damage_to_tower = damage_to_tower
        self.damage_to_player = damage_to_player

    
    def update(self, target, deltatime):
        dir = pygame.Vector2(target) - self.pos

        if dir.length_squared() > 0:
            self.pos += dir.normalize() * self.speed * deltatime   