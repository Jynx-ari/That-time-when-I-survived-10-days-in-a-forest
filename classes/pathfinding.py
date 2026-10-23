import heapq
import math # collections and deque is finally gone but I GOT MATH AGAIN???!?!?

import pygame

def build_flow_field(blocked, goal):
    #ama replace everything.. AGAINN >:((

    height = len(blocked)
    width = len(blocked[0])

    distances = [
        [float("inf") for _ in range(width)]
        for _ in range(height)
    ]

    g_x, g_y = goal

    if not (0 <= g_x < width and 0 <= g_y < height):
        return distances

    if blocked[g_y][g_x]:
        return distances

    distances[g_y][g_x] = 0
    queue = [(0, g_x, g_y)]

    directions = (
        (1, 0, 1.0),
        (-1, 0, 1.0),
        (0, 1, 1.0),
        (0, -1, 1.0),
        (1, 1, math.sqrt(2)),
        (1, -1, math.sqrt(2)),
        (-1, 1, math.sqrt(2)),
        (-1, -1, math.sqrt(2)),
    )

    while queue:
        current_dist, x, y = heapq.heappop(queue)

        if current_dist > distances[y][x]:
            continue

        for dx, dy, cost in directions:
            nx = x + dx
            ny = y + dy

            if not (0 <= nx < width and 0 <= ny < height):
                continue

            if blocked[ny][nx]:
                continue

            # Prevent diagonal movement through blocked corners.
            if dx != 0 and dy != 0:
                if blocked[y][nx] or blocked[ny][x]:
                    continue

            new_dist = current_dist + cost

            if new_dist < distances[ny][nx]:
                distances[ny][nx] = new_dist
                heapq.heappush(queue, (new_dist, nx, ny))

    for y in range(height):
        for x in range(width):
            if distances[y][x] == float("inf"):
                distances[y][x] = None

    return distances


def next_cell_toward_goal(distances, cell):
    """Return a neighboring cell with a lower flow-field distance.

    Diagonal steps are only allowed when both adjacent cardinal cells are
    reachable. This mirrors the corner-blocking rule in build_flow_field().
    """
    height = len(distances)
    if height == 0:
        return None
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

        # A None distance represents a blocked or unreachable cell. If either
        # cardinal neighbor is unavailable, don't cut diagonally across it.
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

    # The tower is blocked, so choose a nearby walkable goal cell.
    target = pygame.Vector2(target_world)
    goal_cell = None
    best_distance = float("inf")

    for y in range(rows):
        for x in range(columns):
            if blocked[y][x]:
                continue

            center = pygame.Vector2(
                x * cell_size + cell_size / 2,
                y * cell_size + cell_size / 2,
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
