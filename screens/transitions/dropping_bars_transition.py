#Referenced by 1993 DOOM i guess and i dont know why i just picked dis cuz its my favourite

import math #MATH IS EVERYWHEREREEEEE!!!!!
import random
import pygame

class DroppingBarsTransition:
    def __init__(self, size, bar_width=20, color=(0,0,0)):
        self.width, self.height = size
        self.bar_width = bar_width
        self.color = color
        self.phase = "idle" # So basically, idle -> cover -> covered -> reveal -> idle
        self.bars=[]
    
    @property
    def active(self):
        return self.phase != "idle"
    
    @property
    def is_covered(self):
        return self.phase == "covered"
    
    def start(self):
        c = math.ceil(self.width/self.bar_width)
        self.bars = [
            {"y": 0.0, "speed": random.randint(10,18) * 60} # px per second!
            for _ in range(c)
        ]
        self.phase = "cover"

    def begin_reveal(self):
        self.phase = "reveal"
    
    def update(self, dt):
        if self.phase not in ("cover", "reveal"):
            return
        
        limit = self.height if self.phase == "cover" else self.height * 2
        finished = True

        for bar in self.bars:
            bar["y"] = min(limit, bar["y"] + bar["speed"] * dt)
            finished = finished and bar["y"] >= limit

        if finished:
            self.phase = "covered" if self.phase == "cover" else "idle"
    
    def draw(self, screen):
        if self.phase == "idle":
            return
        
        for index, bar in enumerate(self.bars):
            x = index * self.bar_width
            if self.phase in ("cover", "covered"):
                top, height = 0, bar["y"]
            else:
                top = bar["y"] - self.height
                height = self.height - top
            
            if height > 0:
                pygame.draw.rect(
                    screen,
                    self.color,
                    (x, int(top), self.bar_width, math.ceil(height))
                )