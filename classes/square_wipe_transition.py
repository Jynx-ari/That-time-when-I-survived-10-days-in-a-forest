import pygame

#inspired by other games idk

class squarewipetransition:
    def __init__(
        self,
        dur=0.8,
        grid=40,
        color=(0,0,0)
    ):
        self.dur = dur
        self.grid_size = grid
        self.color =color

        self.active = False
        self.phase = "closing"
        self.elapsed = 0.0

        self.old_surface = None
        self.on_covered = None
        
