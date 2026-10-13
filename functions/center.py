import pygame

def draw_center(screen, wh, tower_color, antenna_color):
    w, h = wh
    tower_size = 60
    tower_rect = pygame.Rect(
        w // 2 - tower_size // 2,
        h // 2 - tower_size // 2,
        tower_size,
        tower_size,
    )
    antenna_size = 18
    antenna_rect = pygame.Rect(
        tower_rect.centerx - antenna_size // 2,
        tower_rect.centery - antenna_size // 2 ,
        antenna_size,
        antenna_size,
    )

    pygame.draw.rect(screen, tower_color, tower_rect)
    pygame.draw.rect(screen, antenna_color, antenna_rect)