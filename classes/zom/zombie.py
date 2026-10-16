import pygame

class Zombie():
    def __init__(self, pos, health=100, speed=0, damage_to_towers=0.0, damage_to_player=0.0):
        self.pos = pos
        self.health = health
        self.speed = speed
    
    def update(self, target, deltatime):
        dir = pygame.Vector2(target) - self.pos

        if dir.length_squared() > 0:
            self.pos += dir.normalize() * self.speed * dt