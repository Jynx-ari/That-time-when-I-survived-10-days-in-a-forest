from classes.pathfinding import build_flow_field, next_cell_toward_goal

width, height = 7, 7
blocked = [[False] * width for _ in range(height)]

# Wall with an opening at the bottom
for y in range(6):
    blocked[y][3] = True

start = (1, 2)
goal = (5, 2)

field = build_flow_field(blocked, goal)

assert field[start[1]][start[0]] is not None
assert field[start[1]][start[0]] > 4

position = start
route = [position]

while position != goal:
    position = next_cell_toward_goal(field, position)
    assert position is not None, "Route unexpectedly ended!"
    route.append(position)

print("Pathfinding test passed!")
print("Route:", route)
print("Steps:", len(route) - 1)