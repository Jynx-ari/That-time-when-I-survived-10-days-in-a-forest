#bruh another classes for me to do :)))

import pygame

class Obstacle:
    def __init__(self, rect, name="obstacle", blocks_movement=True, blocks_shots=True):
        self.rect = pygame.Rect(rect)
        self.name=name
        self.blocks_movement = blocks_movement
        self.blocks_shots = blocks_shots
        