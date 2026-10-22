import pygame
from ..obstacle import Obstacle

import math #math..
from functions.easing_styles import EasingStyle, EasingDirection
from functions.tween_service import TweenInfo, TweenService

default_conf = {
    "size": 10,
    "walkspeed": 90 #base 90
}


class Player:
    def __init__(self, pos, ws=default_conf["walkspeed"], size=default_conf["size"], max_health=100):
        self.pos = pygame.Vector2(pos)
        self.speed = ws
        self.size = size
        self.angle = 90
        self.max_hp = max_health
        self.hp = self.max_hp #i forgor about this lil guy
        self.display_hp = self.max_hp
        self.health_shake = 0.0
        self.shake_time = 0.0
        self.shake_frequency = 45.0 #uh oh..

        self.tween_service = TweenService()

        self.health_tween_info = TweenInfo(
            dur=0.5,
            easing_style=EasingStyle.QUAD,
            easing_direction=EasingDirection.OUT,
        )
        self.health_shake_info = TweenInfo(
            dur=0.35,
            easing_style=EasingStyle.QUAD,
            easing_direction=EasingDirection.OUT
        )
    

    def update(self, dt):
        self.shake_time += dt
        self.tween_service.update(dt)


    def healthui(self, screen):
        bar_width = 220
        bar_height = 24

        shake_x = math.sin( #sin... horrors of math..
            self.shake_time * self.shake_frequency
        ) * self.health_shake

        shake_y = math.cos(
            self.shake_time * self.shake_frequency * 1.3            
        ) * self.health_shake * 0.35

        x = round(20 + shake_x)
        y = round(
            screen.get_height() - bar_height - 20 + shake_y
        )

        #get ratio'ed
        health_ratio = max(0, min(1, self.hp / self.max_hp))
        display_ratio = max(0, min(1, self.display_hp / self.max_hp))
        current_width = round(bar_width * health_ratio)
        display_width = round(bar_width * display_ratio)


        #emptyy bar!
        pygame.draw.rect(
            screen,
            "#301515",
            (x,y,bar_width, bar_height)
        )

        #delayed damage indicator or thingy
        pygame.draw.rect(
            screen,
            "#f4e8c1",
            (x,y, display_width, bar_height)
        )

        #actual health_ratio
        pygame.draw.rect(
            screen,
            "#d43f3f",
            (x,y,current_width, bar_height)
        )
        
        #white box border
        pygame.draw.rect(
            screen,
            "#f4e8c1",
            (x,y,bar_width, bar_height),
            width=2
        )

    def update_healthbar(self, dt):
        transition_speed =30
        if self.display_hp > self.hp:
            self.display_hp = max(
                self.hp,
                self.display_hp - transition_speed * dt
            )
        else:
            self.display_hp = self.hp


    def take_damage(self, damage_given: int):

        old_hp = self.hp

        self.hp = max(0, self.hp - max(0, damage_given)) #NUH UH  im not letting a god health for the player ( historically: Players that has a negative integer health is basically immortal if the code checks if its health is zero)

        delta_health = old_hp - self.hp
        
        if delta_health > 0:
            self.tween_service.create(
                self,
                self.health_tween_info,
                {"display_hp": self.hp}
            ).play()

            self.health_shake = min(
                14.0,
                max(self.health_shake, delta_health * 1.5)
            )
            self.shake_time = 0.0

            self.tween_service.create(
                self,
                self.health_shake_info,
                {"health_shake":0.0},
            ).play()

        
        return delta_health
      

    @property #i still dont get it how does dis decorator work
    def is_dead(self): #yo is the player still alive??
        return self.hp <= 0

    def move(self, keys, dt, world_size, screen, obstacles=None):
        dir_ = pygame.Vector2(0,0)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dir_.x -= 1
        
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dir_.x +=1

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dir_.y -= 1
        
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dir_.y+=1
        
        
        #HAHA NO DIAGONAL BOOST MOVEMENT!!
        if dir_.length_squared() > 0:
            dir_ = dir_.normalize()

        #obviously...
        if obstacles is None:
            obstacles=[]

        movement = dir_ * self.speed * dt
        #lets try horizontal movement first!1
        next_x = self.pos.x + movement.x

        player_rect = pygame.Rect(
            round(next_x - self.size),
            round(self.pos.y - self.size),
            self.size * 2, self.size * 2,
        )

        #hitbox test
        #pygame.draw.rect(screen, "red", player_rect, 1)

        nearby_obstacles = obstacles.query(player_rect)

        blocked = any(
            obstacle.blocks_movement
            and player_rect.colliderect(obstacle.rect)
            for obstacle in nearby_obstacles
        )

        if not blocked:
            self.pos.x = next_x
        
        #then we go for y axis noww

        next_y = self.pos.y + movement.y

        player_rect = pygame.Rect(

            round(self.pos.x - self.size),
            round(next_y - self.size),
            self.size * 2, 
            self.size * 2,

        )
        nearby_obstacles = obstacles.query(player_rect)
        blocked = any(
            obstacle.blocks_movement
            and player_rect.colliderect(obstacle.rect)
            for obstacle in nearby_obstacles
        )

        if not blocked:
            self.pos.y = next_y

        self.pos.x = max(
            self.size,
            min(self.pos.x,
                world_size[0] - self.size
            )
        )

        self.pos.y = max(
            self.size,
            min(self.pos.y, world_size[1] - self.size)
        )

    
    def aimlook(self, mouse_pos, camera, zoom=1.0):
        # Disney land??
        mouse_world = pygame.Vector2(
            mouse_pos[0] / zoom + camera.offset[0],
            mouse_pos[1] / zoom+ camera.offset[1]
        )

        dir_ = mouse_world - self.pos

        if dir_.length_squared() > 0:
            self.angle = dir_.as_polar()[1]


    def draw(self, screen, screen_pos, zoom=1.0):
        x,y = round(screen_pos[0]), round(screen_pos[1])
        
        size = self.size * zoom

        points = [
            pygame.Vector2(0, -size * 1.6), #pointy thingy!
            pygame.Vector2(-size * 0.8,size * 0.75), # left rer
            pygame.Vector2(size * 0.8,size*0.75) # right rearrrr
 

        ]

        rotated_points = [
            point.rotate(self.angle + 90) + (x,y)
            for point in points
        ]
        pygame.draw.polygon(screen, "#F4E8C1", rotated_points)
        pygame.draw.polygon(
            screen, 
            "#282820", 
            rotated_points,
              width=max(1, round(3*zoom)))


