# HELL YEHH!!! PEW PEW AND BANG BANG!!

import pygame


class HitscanWeapon:
    def __init__(
        self,
        damage=40, #is -35 hp too much..
        max_range = 1500,
        fire_interval=0.17, #cooldown?
        hit_radius=15

    ):

        self.damage = damage
        self.max_range = max_range
        self.fire_interval = fire_interval
        self.hit_r = hit_radius
        self.cooldown = 0.0
        self.tracer_start = None
        self.tracer_end = None
        self.tracer_timer = 0.0
        self.tracer_duration = 0.08

    def update(self, deltaT):
        self.cooldown = max(0.0, self.cooldown - deltaT)

        self.tracer_timer = max(
            0.0,
            self.tracer_timer - deltaT,
        )

        if self.tracer_timer <= 0.0:
            self.tracer_start = None
            self.tracer_end = None
    
    def is_bro_disabled(self):
        return self.cooldown <= 0.0
    
    def PEWPEW(self, origin, target_world, zombies, obstacle_grid, tween_service=None):
        # yes pew pew, returns: (hit_zombie, shot_end) NOTE: hit_zombie is None when the shot misses LMAOO!!

        origin = pygame.Vector2(origin)
        target_world = pygame.Vector2(target_world)

        aim_dir = target_world - origin

        if aim_dir.length_squared() == 0:
            return None, origin
        
        aim_dir = aim_dir.normalize()
        shot_end = origin + aim_dir * self.max_range
        obstruction_dist = self.max_range
        

        ray_rect = pygame.Rect(
            round(min(origin.x, shot_end.x)),
            round(min(origin.y, shot_end.y)),
            max(1, round(abs(shot_end.x - origin.x))),
            max(1, round(abs(shot_end.y - origin.y))),
        )

        for obstacle in obstacle_grid.query(ray_rect):
            if not obstacle.blocks_shots:
                continue
            
            clipped_line = obstacle.rect.clipline(
                (round(origin.x), round(origin.y)),
                (round(shot_end.x), round(shot_end.y))
            )

            if not clipped_line:
                continue

            impact_point = pygame.Vector2(clipped_line[0])
            obstacle_dist = origin.distance_to(impact_point)

            if obstacle_dist < obstruction_dist:
                obstruction_dist = obstacle_dist
                shot_end = impact_point


        if not self.is_bro_disabled():
            return None, shot_end
        
        self.cooldown = self.fire_interval

        nearest_zombie = None
        nearest_dist = self.max_range
        nearest_dist = self.max_range

        for zombie in zombies:
            if zombie.dead:
                continue
            to_zomb = zombie.pos - origin

            #the distance along the shot direction to the closest point or something..
            along_shot = to_zomb.dot(aim_dir)

            if not 0 <= along_shot <= obstruction_dist:
                continue
        
            closest_point = origin+aim_dir*along_shot
            dist_square = zombie.pos.distance_squared_to(
                closest_point
            )

            if dist_square > self.hit_r ** 2:
                continue
                
            if along_shot < nearest_dist:
                nearest_dist = along_shot
                nearest_zombie = zombie
        
        if nearest_zombie is not None:
            shot_end = origin + aim_dir *nearest_dist
            nearest_zombie.DIE_ZOMBIE_DIE(self.damage, tween_service, aim_dir)

        self.tracer_start = origin.copy()
        self.tracer_end = shot_end.copy()
        self.tracer_timer = self.tracer_duration


        return nearest_zombie, shot_end
    
    def draw(self,screen,camera,zoom):
        if self.tracer_start is None or self.tracer_end is None:
            return
        start_screen = camera.syncworld_to_screen(
            self.tracer_start,
            zoom,
        )

        end_screen = camera.syncworld_to_screen(
            self.tracer_end,
            zoom,
        )

        pygame.draw.line( # LINE!!
            screen,
            "#FCC01E",
            (round(start_screen[0]), round(start_screen[1])),
            (round(end_screen[0]), round(end_screen[1])),
            max(1, round(3 * zoom)),
        ) 