#import pygame

class Camera:
    def __init__(self, offset=(0,0)):
        self.offset = offset

    def syncworld_to_screen(self, pos):
        return (
            pos[0] - self.offset[0],
            pos[1] - self.offset[1],
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

    def follow(self, target_pos, world_size, viewport_size):
        max_x = world_size[0] - viewport_size[0]
        max_y = world_size[1] - viewport_size[1]

        self.offset=(
            max(
                0,
                min(
                    target_pos[0] - viewport_size[0] / 2, max_x
                )
            ),
            max(
                0,
                min(
                    target_pos[1] - viewport_size[1] / 2, max_y
                )
            )
        )