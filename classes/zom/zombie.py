import pygame

default_config = {
    "zombie size": 15
}


class Zombie():
    def __init__(self, pos, health=100, speed=0, damage_to_tower=0.0, damage_to_player=0, attack_cd=0.0, attack_interval = 1.2):
        self.pos = pygame.Vector2(pos)
        self.health = health
        self.speed = speed
        self.damage_to_tower = damage_to_tower
        self.damage_to_player = damage_to_player
        self.attack_cooldown = attack_cd
        self.attack_interval = attack_interval
        


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

    

    def can_attack(self, deltaT):
        self.attack_cooldown = max(0, self.attack_cooldown - deltaT)

        if self.attack_cooldown > 0:
            return False

        self.attack_cooldown = self.attack_interval
        return True




    def update(self, target, deltatime, obstacles=None):

        if obstacles is None:
            obstacles = []
        
        target = pygame.Vector2(target)
        dir_ = pygame.Vector2(target) - self.pos

        if dir_.length_squared() == 0:
            return
        
        dir_ = dir_.normalize()
        movement = dir_*self.speed*deltatime

        #movement stuffiess!!
        candidates = [

            movement,
            pygame.Vector2(-movement.y, movement.x),
            pygame.Vector2(movement.y, -movement.x),

        ]

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
        



    def draw(self, screen, camera, zoom):
        screen_pos = camera.syncworld_to_screen(self.pos, zoom)

        pygame.draw.circle(
            screen,
            "#7f9f45",
            (round(screen_pos[0]), round(screen_pos[1])),
            max(5, round(15 * zoom))
        )