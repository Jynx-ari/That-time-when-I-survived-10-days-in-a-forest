import pygame

def draw_center(screen, center_pos, tower_color, antenna_color, grass_color,zoom=1.0):

    center_x, center_y = center_pos
    tower_size = max(1, round(42 * zoom))
    tower_rect = pygame.Rect(
        center_x - 2 - tower_size // 2,
        center_y - 2 - tower_size // 2,
        tower_size,
        tower_size,
    )
    antenna_size = max(1, round(12.60 * zoom))

    antenna_rect = pygame.Rect(
        tower_rect.centerx - antenna_size // 2,
        tower_rect.centery - antenna_size // 2 ,
        antenna_size,
        antenna_size,
    )

    dirt_size = max(1, round(800 * zoom))

    dirt_area = pygame.Rect(
            center_x - 2 - dirt_size // 2,
            center_y - 2 - dirt_size // 2,
            dirt_size,
            dirt_size,
        )

    transition_width = max(5, round(100 * zoom))
    band_count = 5
    #steps = transition_width + 1
    band_width = transition_width // band_count
    dirt_color = pygame.Color("#967332")
    grass_color = pygame.Color(grass_color)
   
    pygame.draw.rect(screen, dirt_color, dirt_area)

    for band in range(band_count):
        amount = band / (band_count -1)
        inset = band * band_width
        edge_rect = dirt_area.inflate(-2*inset,-2*inset)
        color = grass_color.lerp(dirt_color, amount)
        pygame.draw.rect(screen, color, edge_rect, width=band_width)

    pygame.draw.rect(screen, tower_color, tower_rect)
    pygame.draw.rect(screen, antenna_color, antenna_rect)