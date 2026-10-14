import pygame

class camera:
    def __init__(self, offset=(0,0)):
        self.offset = offset

    def syncworld_to_screen(self, pos):
        return (
            position[0] - self.offset[0],
            position[1] - self.offset[1],
        )
