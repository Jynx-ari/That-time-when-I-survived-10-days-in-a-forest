from collections import deque #not this again.. (For lore, i made a path finding thingy with the help of AI coding as my 2nd prep week project but I got bored so i switched to making this game)

import pygame

def build_flow_field(blocked, goal):
    # Basically Calculate each walkable cell's distance from the goal using.... BFS..abs
    # Well we're gonna make the map as a grid for checking stuffs
    height = len(blocked)
    width = len(blocked[0])

    distances = [
        [None for _ in range(width)]
        for _ in range(height)
    ]

    goal_x, goal_y = goal

    if not (0<=goal_x<width and 0<=goal_y<height):
        return distances
    
    if blocked[goal_y][goal_x]:
        return distances

    
    distances[goal_y][goal_x] = 0

    queue=deque([(goal_x, goal_y)])

    directions = (
        (1,0),
        (-1,0),
        (0,1),
        (0,-1),
    )

    while queue:
        x,y = queue.popleft()

        for dx,dy in directions:
            nx=x+dx
            ny=y+dy

            if not (0<=nx < width and 0<=ny<height):
                continue

            if blocked[ny][nx]:
                continue 
            if distances[ny][nx] is not None:
                continue
            
            distances[ny][nx] = distances[y][x] + 1
            queue.append((nx,ny))
    return distances        
            
def next_cell_toward_goal(distances, cell):
    # Returns the neighboring cell closer to the goal, or idk none probably

    height = len(distances)
    width = len(distances[0])

    x,y = cell

    if not (0<=x<width and 0<=y<height):
        return None
    
    current_dist = distances[y][x]

    if current_dist is None or current_dist == 0:
        return None
    
    directions = (
        (1,0),
        (-1,0),
        (0,1),
        (0,-1),
    )

    for_distance = []

    for dx,dy in directions:
        nx=x+dx
        ny=y+dy

        if not (0<=nx<width and 0<=ny<height):
            continue

        distance = distances[ny][nx]

        if distance is not None and distance<current_dist:
            for_distance.append((distance, (nx,ny)))
    
    if not for_distance:
        return None
    
    return min(for_distance, key=lambda option: option[0])[1] #bruh whats lambda..???


def build_world_flow_field(
    obstacle_grid,
    world_size,
    target_world,
    cell_size=64,
    zombie_radius=15,
    goal_radius=80,
):
    #uh... yes nav field for zombi!!

    world_width, world_height = world_size

    columns = world_width//cell_size
    rows = world_height//cell_size

    blocked = [
        [False] * columns
        for _ in range(rows)

    ]

    for y in range(rows):
        for x in range(columns):
            center = pygame.Vector2(
                x * cell_size + cell_size / 2,
                y * cell_size + cell_size / 2,
            )

            zombie_rect = pygame.Rect(
                round(center.x - zombie_radius),
                round(center.y - zombie_radius),
                zombie_radius * 2,
                zombie_radius * 2,
            )

            nearby = obstacle_grid.query(zombie_rect)
            blocked[y][x]=any(
                obstacle.blocks_movement
                and zombie_rect.colliderect(obstacle.rect)
                for obstacle in nearby
            )

    #I mean, the tower itself is blocked, so choose a nearby walkable area or something?

    target = pygame.Vector2(target_world)
    goal_cell=None
    best_distance = float("inf")


    max_goal_cells = (goal_radius / cell_size) ** 2

    for y in range(rows):
        for x in range(columns):
            if blocked[y][x]:
                continue
            
            center=pygame.Vector2(
                x*cell_size + cell_size /2,
                y*cell_size + cell_size /2,

            )

            distance = center.distance_squared_to(target)

            if distance > goal_radius ** 2:
                continue

            if distance < best_distance:
                best_distance = distance
                goal_cell = (x, y)
            
    if goal_cell is None:
        return (
            [[None] * columns for _ in range(rows)],
            None,

        )

    return build_flow_field(blocked, goal_cell), goal_cell