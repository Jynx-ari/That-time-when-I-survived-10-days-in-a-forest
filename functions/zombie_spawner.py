import math
import random
import pygame


from classes.zom.shambler import Shambler

def spawn_shamblers(
    amount,
    world_size,
    obstacles=None,
    center=None,
    min_spawn_distance=500,
    max_spawn_distance=1800,
):
    #bruh.. full rewrite again!
    zombies = []
    obstacles = obstacles or []


    if center is None:
        center = pygame.Vector2(
            world_size[0]/2,
            world_size[1] /2,
        )
    else:
        center=pygame.Vector2(center)



    for _ in range(amount):
        for attempt in range(100):

            angle = random.uniform(0, math.tau)
            distance = random.uniform(
                min_spawn_distance,
                max_spawn_distance
            )



            pos = center + pygame.Vector2(
                math.cos(angle),
                math.sin(angle),
            ) * distance

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