import math
import random
import pygame


from classes.zom.shambler import Shambler

def spawn_shamblers(
    amount,
    center,
    min_radius,
    max_radius,
    world_size,
    obstacles=None
):
    zombies = []
    obstacles = obstacles or []

    for _ in range(amount):
        for attempt in range(100):
            angle = random.uniform(0, math.tau) #wats tau???
            radius = random.uniform(min_radius, max_radius)

            pos = pygame.Vector2(
                center[0] + math.cos(angle) * radius, #math is haunting me...
                center[1] + math.sin(angle) * radius

            )

            if not (
                40 <= pos.x <=world_size[0] - 40 
                and 40 <=pos.y<=world_size[1]-40
            ):
                continue

            #do i code weird??

            zombie_rect = pygame.Rect(
                round(pos.x - 15),
                round(pos.y - 15),
                30,
                30
            )

            if any (zombie_rect.colliderect(obstacle.rect) for obstacle in obstacles):
                continue
                
            zombies.append(Shambler(pos))

            break
    return zombies
    