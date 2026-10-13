import pygame

default_trunk = [
    10, #width
    40, #height
    (85, 58, 37), #color
]
default_leaves=[
    (17, 38, 25), #color
    22, #size
]


class gen_Tree():
    def __init__(self, position, treeconfig=None):
        self.trunk_pos = (position[0] - 5, position[1] + 12)
        if treeconfig is not None:
#             CONFIG:
#             [ (width, height), t_color, l_color, l_size ]

            self.trunk_size = treeconfig[0]
            self.trunk_color = treeconfig[1]
            self.leaves_pos = position
            self.leaves_color = treeconfig[2]
            self.leaves_size = treeconfig[3]
        else:
            self.trunk_size = default_trunk[0], default_trunk[1]
            self.trunk_color = default_trunk[2]
            self.leaves_pos = position
            self.leaves_color = default_leaves[0]
            self.leaves_size = default_leaves[1]

    
    def draw(self, screen):
        self.trunk = pygame.draw.rect(screen, self.trunk_color, (self.trunk_pos, self.trunk_size))
        self.leaves = pygame.draw.circle(screen, self.leaves_color, (self.leaves_pos), 22)