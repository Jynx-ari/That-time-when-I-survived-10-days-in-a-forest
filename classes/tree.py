
import pygame

default_trunk = [
    10,                 # Width
    10,                 # Height
    "#7B381A",       # Color
]

default_leaves = [
    "#39752A",       # Color
    22,                 # Radius
]



class gen_Tree:
    def __init__(self, position, treeconfig=None, tree_scale = 0.2):

        scale = max(0.0, min(1.0, tree_scale))
        size_multiplier = 1.0 + scale * 0.5
        self.leaves_pos = position

        if treeconfig is not None:
            # Format: [(width, height), trunk_color, leaves_color, leaves_radius]
            self.trunk_size = treeconfig[0]
            self.trunk_color = treeconfig[1]
            self.leaves_color = treeconfig[2]
            self.leaves_size = treeconfig[3]
        else:
            self.trunk_size = (default_trunk[0], default_trunk[1])
            self.trunk_color = default_trunk[2]
            self.leaves_color = default_leaves[0]
            self.leaves_size = default_leaves[1]

        self.trunk_size = round(self.trunk_size[0] * size_multiplier), round(self.trunk_size[1] * size_multiplier)
        self.trunk_pos = (
            position[0] - self.trunk_size[0] /2,
            position[1] - self.trunk_size[1]/2
        )
        self.leaves_size = round(self.leaves_size * size_multiplier)

    # def draw(self, screen):
    #     pygame.draw.rect(
    #         screen,
    #         self.trunk_color,
    #         (*self.trunk_pos, *self.trunk_size),
    #     )
        
    #     pygame.draw.circle(
    #         screen,
    #         self.leaves_color,
    #         self.leaves_pos,
    #         self.leaves_size,
    #     )
    def draw_trunk(self, screen, screen_pos=None, zoom=1.0):
        if screen_pos is None:
            screen_pos = self.trunk_pos

        x,y = screen_pos
        w, h = self.trunk_size

        trunk_rect = pygame.Rect(
            round(x),
            round(y),
            max(1,
                round(w * zoom)
                ),
            max(1,
                round(h * zoom)
            )
        )

        pygame.draw.rect(
            screen, 
            self.trunk_color,
            trunk_rect,
        )
    
    def draw_leaves(self, screen, screen_pos=None, zoom=1.0, transparent=False):
        if screen_pos is None:
            screen_pos = self.leaves_pos
        
        x,y = round(screen_pos[0]), round(screen_pos[1])
        radius = max(1, round(self.leaves_size *zoom))

        if transparent:
            canopy = pygame.Surface(
                (radius * 2 + 2, radius * 2+ 2),
                pygame.SRCALPHA
            )
            color = pygame.Color(self.leaves_color)
            leaf_color = (color.r, color.g, color.b, 100)

            pygame.draw.circle(
                canopy,
                leaf_color,
                (radius + 1, radius + 1),
                radius,
            )
            screen.blit(
                canopy, 
                (x-radius-1, y-radius-1)
            )
        else:
            pygame.draw.circle(
                screen,
                self.leaves_color,
                (x,y),
                radius,

            )