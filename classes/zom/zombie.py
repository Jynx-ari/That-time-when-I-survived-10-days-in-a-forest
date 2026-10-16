import pygame

class Zombie():
    def __init__(self, pos, health=100, speed=0, damage_to_tower=0.0, damage_to_player=0.0):
        self.pos = pygame.Vector2(pos)
        self.health = health
        self.speed = speed
        self.damage_to_tower = damage_to_tower
        self.damage_to_player = damage_to_player

    
    def update(self, target, deltatime):
        dir_ = pygame.Vector2(target) - self.pos

        if dir_.length_squared() > 0:
            self.pos += dir_.normalize() * self.speed * deltatime   

    def draw(self, screen, camera, zoom):
        screen_pos = camera.syncworld_to_screen(self.pos, zoom)

        pygame.draw.circle(
            screen,
            "#7f9f45",
            (round(screen_pos[0]), round(screen_pos[1])),
            max(5, round(15 * zoom))
        )