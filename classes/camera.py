import pygame

class Camera:
    def __init__(self, offset=(0,0)):
        self.offset = offset

    def syncworld_to_screen(self, pos):
        return (
            pos[0] - self.offset[0],
            pos[1] - self.offset[1],
        )
