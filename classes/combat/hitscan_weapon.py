# HELL YEHH!!! PEW PEW AND BANG BANG!!

import pygame


class HitscanWeapon:
    def __init__(
        self,
        damage=35, #is -35 hp too much..
        max_range = 500,
        fire_interval=0.35, #cooldown?
        hit_radius=15

    ):

        self.damage = damage
        self.max_range = max_range
        self.fire_interval = fire_interval
        self.hit_r = hit_radius
        self.cooldown = 0.0

    def update(self, deltaT):
        self.cooldown = max(0.0, self.cooldown - deltaT)
    
    def is_bro_disabled(self):
        return self.cooldown <= 0.0
    
    def PEWPEW(self, origin, target_world, zombies):
        # yes pew pew, returns: (hit_zombie, shot_end) NOTE: hit_zombie is None when the shot misses LMAOO!!

        origin = pygame.Vector2(origin)
        target_world = pygame.Vector2(target_world)

        aim_dir = target_world - origin

        if aim_dir.length_squared() == 0:
            return None, origin
        
        aim_dir = aim_dir.normalize()
        shot_end = origin + aim_dir * self.max_range

        if not self.is_bro_disabled():
            return None, shot_end
        
        self.cooldown = self.fire_interval

        nearest_zombie = None
        nearest_dist = self.max_range

        for zombie in zombies:
            to_zomb = zombie.pos - origin

            #the distance along the shot direction to the closest point or something..
            along_shot = to_zomb.dot(aim_dir)

            if not 0 <= along_shot <= self.max_range:
                continue
        
            closest_point = origin+aim_dir*along_shot
            dist_square = zombie.pos.distance_squared.to(
                closest_point
            )

            if dist_square > self.hit_r ** 2:
                continue
                
            if along_shot < nearest_dist:
                nearest_dist = along_shot
                nearest_zombie = zombie
        
        if nearest_zombie is not None:
            shot_end = origin + aim_dir *nearest_dist
            nearest_zombie.DIE_ZOMBIE_DIE(self.damage)

        return nearest_zombie, shot_end