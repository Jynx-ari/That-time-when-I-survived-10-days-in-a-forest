import math
import random
import pygame


from classes.zom.shambler import Shambler

def spawn_shamblers(
    amount,
    world_size,
    obstacles=None
):
    #bruh.. full rewrite again!
    zombies = []
    obstacles = obstacles or []

    for _ in range(amount):
        for attempt in range(100):
            pos = pygame.Vector2(
                random.uniform(40, world_size[0] -40),
                random.uniform(40, world_size[1]- 40),
            )

            zombie_rect = pygame.Rect(
                round(pos.x - 15),
                round(pos.y - 15),
                30,
                30,
            )

            #HELL NO DONT SPAWN INSIDE A TREE TRUNK OR THE TOWER??
            if any(
                zombie_rect.colliderect(obstacle.rect)
                for obstacle in obstacles
            ): 
                continue

            zombies.append(Shambler(pos))
            break
    return zombies