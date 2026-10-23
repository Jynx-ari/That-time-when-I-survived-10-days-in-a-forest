import pygame
from classes.pathfinding import next_cell_toward_goal

from functions.tween_service import TweenInfo
from functions.easing_styles import EasingDirection, EasingStyle

default_config = {
    "zombie size": 15
}


class Zombie():
    def __init__(self, pos, health=100, speed=0, damage_to_tower=0.0, damage_to_player=0.0, attack_cd=0.0, attack_interval = 1.2):
        self.pos = pygame.Vector2(pos)

        self.direction = pygame.Vector2(0,0)
        self.turn_speed = 5.0

        self.health = health
        self.speed = speed
        self.damage_to_tower = damage_to_tower
        self.damage_to_player = damage_to_player
        self.attack_cooldowns = {
            "tower": attack_cd,
            "player": attack_cd,
        }
        self.attack_interval = attack_interval
        self.dead = False #how quite the irony..
        self.hit_flash_timer = 0.0 #ka-ching!
        self.hit_flash_duration = 0.12
        self.hit_flash_strength = 0.0
        self.hit_flash_tween = None

        self.hit_speed_multiplier = 1.0
        self.knockback_vel_x = 0.0
        self.knockback_vel_y = 0.0
        self.hit_motion_tween = None


    def is_blocked(self, pos, obstacles):
        zombie_size = default_config["zombie size"]
        zomb_rect = pygame.Rect(
            round(pos.x - zombie_size),
            round(pos.y - zombie_size),
            zombie_size * 2,
            zombie_size * 2
        )
        nearby_obstacles = obstacles.query(zomb_rect)
        return any(
            obstacle.blocks_movement
            and zomb_rect.colliderect(obstacle.rect)
            for obstacle in nearby_obstacles
        )

    

    def can_attack(self, deltaT, target):
        cd = max(0, self.attack_cooldowns[target] - deltaT)

        self.attack_cooldowns[target] = cd

        if cd > 0:
            return False
        
        self.attack_cooldowns[target] = self.attack_interval
        return True



    def update(self, target, deltatime, obstacles=None, flow_field=None, cell_size=64):
        

        if obstacles is None:
            obstacles = []
        
        target = pygame.Vector2(target)

        if flow_field is not None:
            cell_x = int(self.pos.x // cell_size)
            cell_y = int(self.pos.y // cell_size)

            if (
                0<= cell_y < len(flow_field)
                and 0 <= cell_x < len(flow_field[0])
            ): 
                # current_distance = flow_field[cell_y][cell_x]

                # if current_distance == 0:
                #     return
                
                next_cell = next_cell_toward_goal(
                    flow_field,
                    (cell_x, cell_y)
                )


                if next_cell is not None:
                    n_x, n_y = next_cell

                    #uhhh idk
                    target = pygame.Vector2(
                        n_x * cell_size + cell_size / 2,
                        n_y * cell_size + cell_size / 2,
                    )

        # I hope yall get the reference of wish dir (Quake and Source)
        wishdir = target - self.pos

        if wishdir.length_squared() == 0:
            return
        wishdir = wishdir.normalize()

        if self.direction.length_squared() == 0:
            self.direction = wishdir
        else:
            turn_amount = min(1.0, self.turn_speed * deltatime)

            self.direction = self.direction.lerp(
                wishdir,
                turn_amount
            ).normalize()
        
        movement = (
            self.direction
            * self.speed
            * self.hit_speed_multiplier
            * deltatime
        )
        

        #movement stuffiess!!
        candidates = [

            # movement,
            # pygame.Vector2(-movement.y, movement.x), #slide to the one side
            # pygame.Vector2(movement.y, -movement.x), # slide to the other side just checking
            # pygame.Vector2(movement.x, 0), #try horizontal
            # pygame.Vector2(0,movement.y) #try vertical
            

        ]

        for angle in (0,30,-30,60,-60,90,-90,135,-135, 180):
            candidate = movement.rotate(angle)
            candidates.append(candidate)

        best_move = None
        best_distance = float("inf")

        for candidate in candidates:
            next_pos = self.pos + candidate

            if self.is_blocked(next_pos, obstacles):
                continue
                
            distance = next_pos.distance_squared_to(target)

            if distance < best_distance:
                best_distance = distance
                best_move = candidate
        
        if best_move is not None:
            self.pos += best_move
        
        # else:
        #     print("One of the zoms stuck at: ", round(self.pos.x), round(self.pos.y))

        knockback_move = pygame.Vector2(
            self.knockback_vel_x,
            self.knockback_vel_y,
        ) * deltatime

        if knockback_move.length_squared() > 0:
            knockback_pos = self.pos + knockback_move
            
            if not self.is_blocked(knockback_pos, obstacles):
                self.pos = knockback_pos


        
        



    def draw(self, screen, camera, zoom):
        screen_pos = camera.syncworld_to_screen(self.pos, zoom)

        normal_color = pygame.Color("#7f9f45")
        flash_color = pygame.Color("#ffffff")

        color = normal_color.lerp(
            flash_color,
            self.hit_flash_strength,
        )

        pygame.draw.circle(
            screen,
            color,
            (round(screen_pos[0]), round(screen_pos[1])),
            max(5, round(15 * zoom))
        )
    
    def DIE_ZOMBIE_DIE(self, damage, tween_service=None,knockback_direction=None):
        if self.dead:
            return #really? a zombie? dead??
        self.health = max(0, self.health - damage)


        if tween_service is not None:
            if self.hit_flash_tween is not None:
                self.hit_flash_tween.cancel()
            
            self.hit_flash_strength = 1.0

            self.hit_flash_tween = tween_service.create(
                self,
                TweenInfo(
                    self.hit_flash_duration,
                    EasingStyle.QUAD,
                    EasingDirection.OUT,
                ),
                {"hit_flash_strength": 0.0}
            )

            self.hit_flash_tween.play()
        if tween_service is not None and knockback_direction is not None:
            if self.hit_motion_tween is not None:
                self.hit_motion_tween.cancel()
            
            knockback_direction = pygame.Vector2(knockback_direction)

            if knockback_direction.length_squared() > 0:
                knockback_direction = knockback_direction.normalize()

                knockback_speed = 220.0
                self.knockback_vel_x = knockback_direction * knockback_speed
                self.knockback_vel_y = knockback_direction * knockback_speed
                self.hit_speed_multiplier = 0.45

                self.hit_motion_tween = tween_service.create(
                    self,
                    TweenInfo(0.35,
                    EasingStyle.QUAD,
                    EasingDirection.OUT
                    ),
                    {"knockback_vel_x": 0.0,
                     "knockback_vel_y": 0.0,
                     "hit_speed_multiplier": 1.0,
                    }
                )

                self.hit_motion_tween.play()



        if self.health <= 0:
            self.dead = True


    