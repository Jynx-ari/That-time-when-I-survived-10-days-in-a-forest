#import pygame
import math #MATHHH1?!?!?!?
class Camera:
    def __init__(self, offset=(0,0)):
        self.offset = offset
        
        self.shake_x = 0.0
        self.shake_y = 0.0


    def syncworld_to_screen(self, pos, zoom=1.0):
        return (
            (pos[0] - self.offset[0]) * zoom + self.shake_x,
            (pos[1] - self.offset[1]) * zoom + self.shake_y,
        )

    def move(self, dxy , world_size, viewport_size):
        dx,dy = dxy

        max_x = world_size[0] - viewport_size[0]
        max_y = world_size[1] - viewport_size[1]

        self.offset = (
            max(
                0, min(
                    self.offset[0] + dx, max_x
                )
            ),
            max(
                0, min(
                    self.offset[1] + dy, max_y
                )

            ),
        )

    def follow(self, target_pos, world_size, viewport_size, dt, smoothness=8.0):
        max_x = world_size[0] - viewport_size[0]
        max_y = world_size[1] - viewport_size[1]

        target_x = max(
            0,
            min(target_pos[0] - viewport_size[0] / 2, max_x)
        )

        target_y = max(
            0,
            min(target_pos[1] - viewport_size[1] / 2, max_y)
        )

        alpha = 1 - math.exp(-smoothness * dt)
        #alpha??!

        current_x, current_y = self.offset
        
        self.offset = (
            current_x + (target_x - current_x) * alpha,
            current_y + (target_y - current_y) * alpha
        )