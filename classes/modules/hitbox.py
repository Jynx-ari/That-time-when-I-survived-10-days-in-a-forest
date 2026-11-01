#yezzir hitbox!

from dataclasses import dataclass, field #field is new??
from typing import Callable #okay wth is this??

import pygame

@dataclass
class OverlapParams: #Inspired by roblox hitbox module (not the built in one, cuz the built in one SUCKS!)
    names: frozenset[str] | None = None # I still forget what does frozenset does
    ignore : set = field(default_factory=set)
    blocks_movement : bool | None = None
    blocks_shots : bool | None = None
    predicate : Callable | None = None  #custom checks?

    def allows(self, obstacle):
        if obstacle in self.ignore:
            return False
        if self.names is not None and obstacle.name not in self.names:
            return False
        if (
            self.blocks_movement is not None
            and obstacle.blocks_movement != self.blocks_movement
        ):
            return False
        if (
            self.blocks_shots is not None
            and obstacle.blocks_shots != self.blocks_shots
        ):
            return False
        if self.predicate is not None and not self.predicate(obstacle):
            return False
        return True

def _closest_point_on_rect(point, rect):
    return pygame.Vector2(
        max(rect.left, min(point.x, rect.right)),
        max(rect.top, min(point.y, rect.bottom))
    )

def query_rect(grid, rect, params=None):
    #aw hell nah
    params = params or OverlapParams()
    return [
        o for o in grid.query(rect)
        if rect.colliderect(o.rect) and params.allows(o)
    ]

def query_circle(grid, center, rad, params=None):
        params = params or OverlapParams()
        center = pygame.Vector2(center)

        box = pygame.Rect(0, 0, rad * 2, rad * 2)
        box.center = center

        return [
            obstacle
            for obstacle in grid.query(box)
            if params.allows(obstacle)
            and _closest_point_on_rect(
                center,
                obstacle.rect,
            ).distance_to(center) <= rad
        ]

def query_cone(grid, origin, facing_deg, reach, half_ang_deg, params=None):
    origin = pygame.Vector2(origin)
    facing = pygame.Vector2(1, 0).rotate(facing_deg)
    hits = []

    for obstacle in query_circle(grid, origin, reach, params):
        target = _closest_point_on_rect(origin, obstacle.rect)
        to_target = target - origin

        if to_target.length_squared() == 0:
            angle = 0
        else:
            angle = abs(facing.angle_to(to_target))

        if angle <= half_ang_deg:
            hits.append((to_target.length_squared(), obstacle))

    hits.sort(key=lambda pair: pair[0])
    return [obstacle for _, obstacle in hits]
