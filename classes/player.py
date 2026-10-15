import pygame

default_conf = {
    "size": 10,
    "walkspeed": 90
}


class Player:
    def __init__(self, pos, ws=default_conf["walkspeed"], size=default_conf["size"]):
        self.pos = pygame.Vector2(pos)
        self.speed = ws
        self.size = size
        self.angle = 90

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
    
    def aimlook(self, mouse_pos, camera, zoom=1.0):
        # Disney land??
        mouse_world = pygame.Vector2(
            mouse_pos[0] / zoom + camera.offset[0],
            mouse_pos[1] / zoom+ camera.offset[1]
        )

        dir = mouse_world - self.pos

        if dir.length_squared() > 0:
            self.angle = dir.as_polar()[1]


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
