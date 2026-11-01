import heapq
import math # collections and deque is finally gone but I GOT MATH AGAIN???!?!?

import pygame

def build_flow_field(blocked, goal_cells):
    #ama replace everything.. AGAINN >:(( AND AGAINN

    h  = len(blocked)
    w =  len(blocked[0])

    d = [[None] * w for _ in range(h)]
    queue = []
    dir_s = (
          (1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0),
        (1, 1, math.sqrt(2)), (1, -1, math.sqrt(2)),
        (-1, 1, math.sqrt(2)), (-1, -1, math.sqrt(2)),
    )
    
    #my arms hurt for rewriting code 
    #seed search!!

    for gx, gy in goal_cells:
        if not(0<=gx<w and 0<=gy<h):
            continue
        if blocked[gy][gx]:
            continue
        
        d[gy][gx] = 0
        heapq.heappush(queue, (0,gx,gy))

    while queue:
        current_dist , x,y = heapq.heappop(queue)

        if current_dist > d[y][x]:
            continue

        for dx,dy, cost in dir_s:
            nx,ny = x+dx, y+dy

            if not(0<=nx<w and 0<=ny<h):
                continue
            if blocked[ny][nx]:
                continue
            # NO DIAGONAL!
            if dx != 0 and dy != 0:
                if blocked[y][nx] or blocked[ny][x]:
                    continue
            
            new_dist = current_dist + cost
            old_dist = d[ny][nx]
            if old_dist is None or new_dist<old_dist:
                d[ny][nx] = new_dist
                heapq.heappush(queue, (new_dist, nx,ny))
    return d


def next_cell_toward_goal(distances, cell):
    height = len(distances)
    width = len(distances[0])

    x, y = cell

    if not (0 <= x < width and 0 <= y < height):
        return None

    current_dist = distances[y][x]

    if current_dist is None or current_dist == 0:
        return None

    directions = (
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1),
    )

    candidates = []

    for dx, dy in directions:
        nx = x + dx
        ny = y + dy

        if not (0 <= nx < width and 0 <= ny < height):
            continue

        distance = distances[ny][nx]

        if distance is None or distance >= current_dist:
            continue

        #smol tweaks here
        if dx != 0 and dy != 0:
            if distances[y][nx] is None or distances[ny][x] is None:
                continue

        candidates.append((distance, (nx, ny)))

    if not candidates:
        return None

    return min(candidates, key=lambda option: option[0])[1]


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

    columns = world_width // cell_size
    rows = world_height // cell_size

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
            blocked[y][x] = any(
                obstacle.blocks_movement
                and zombie_rect.colliderect(obstacle.rect)
                for obstacle in nearby
            )

    # I mean, the tower itself is blocked, so choose a nearby walkable area or something?

    target = pygame.Vector2(target_world)
    goal_cells = set()

    for y in range(rows):
        for x in range(columns):
            if blocked[y][x]:
                continue
            
            center = pygame.Vector2(
                x * cell_size + cell_size / 2,
                y * cell_size + cell_size / 2
            )

            if center.distance_to(target) <= goal_radius:
                goal_cells.add((x,y))
        
    if not goal_cells:
        return [[None]*columns for _ in range(rows)], set()
            

        

    return build_flow_field(blocked, goal_cells),goal_cells    
