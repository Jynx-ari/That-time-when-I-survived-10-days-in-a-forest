
import pygame

default_trunk = [
    10,                 # Width
    50,                 # Height
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
        self.trunk_pos = (position[0] - 5, position[1] + 12)
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
    def draw_trunk(self, screen):
        
        pygame.draw.rect(screen, 
        self.trunk_color, 
        (*self.trunk_pos, *self.trunk_size)
        )
    
    def draw_leaves(self, screen):
        pygame.draw.circle(
            screen,
            self.leaves_color,
            self.leaves_pos,
            self.leaves_size,
        )