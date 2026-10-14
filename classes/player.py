import pygame

default_conf = {
    "size": 14,
    "walkspeed": 220
}


class Player:
    def __init__(self, pos, ws=default_conf["walkspeed"], size=default_conf["size"]):
        self.pos = pygame.Vector2(pos)
        self.speed = ws
        self.size = size

    def move(self, keys, dt, world_size):
        dir = pygame.Vector2(0,0)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dir.x -= 1
        
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dir.x +=1

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dir.y -= 1
        
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dir.y+=1
        
        #HAHA NO SOURCE MOVEMENT!!
        if dir.length_squared() > 0:
            dir = dir.normalize()

        self.pos += dir * self.speed * dt

        self.pos.x = max(
            self.size,
            min(
                self.pos.x,
                world_size[0] - self.size
            )
        )

        self.pos.y = max(
            self.size,
            min(
                self.pos.y,
                world_size[1] - self.size
            )
        )
    
    def draw(self, screen, screen_pos):
        x,y = screen_pos
        size = self.size

        points = [
            (x, y - size),
            (x - size, y + size),
            (x + size, y + size),
        ]
        pygame.draw.polygon(screen, "#F4E8C1", points)
        pygame.draw.polygon(screen, "#282820", points, width=3)
