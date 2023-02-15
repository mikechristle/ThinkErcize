# ---------------------------------------------------------------------------
# Best Route
# Find the shortest route that gets all dogs home.
# Mike Christle 2023
# ---------------------------------------------------------------------------

from threading import Thread
from collections import namedtuple
from copy import deepcopy
from cell import Cell

import state as st

LARGE_INT = 1000000

Loc = namedtuple('Loc', ['x', 'y', 'val'])
car_loc = Loc(0, 0, 0)
maze = [[Cell(0, 0)]]
dists = [[0 for _ in range(17)] for _ in range(17)]
locs = []
car = []
indices = []
min_dist = 0


# ---------------------------------------------------------------------------
def find_shortest_route():
    """Start a background thread to determine the shortest route."""

    global maze, car_loc

    car_loc = Loc(st.car_x, st.car_y, 1)
    st.least_miles = 0
    maze = deepcopy(st.maze)
    Thread(target=bg_thread).start()


# ---------------------------------------------------------------------------
def bg_thread():
    """Determine the shourtest route length."""

    global indices, min_dist

    find_objects()
    indices = [x for x in range(1, (st.level * 2) + 1)]
    min_dist = LARGE_INT

    for _ in range(len(indices)):
        next_idx = indices.pop(0)
        dist = get_best_dist(0, next_idx, 0)
        indices.append(next_idx)
        if dist < min_dist:
            min_dist = dist

    st.least_miles = min_dist


# ---------------------------------------------------------------------------
def get_best_dist(from_idx, to_idx, to_dist):
    """Recursive routine to find shortest distances."""

    to_loc = locs[to_idx]

    # Abort if loc has a dog and car is full
    if to_loc.val >= 20 and len(car) > 2:
        return LARGE_INT

    # Abort if loc has a house and dog in not in car
    if 20 > to_loc.val >= 10 and to_loc.val not in car:
        return LARGE_INT

    # Abort if current distance exceeds current minimum
    current_dist = dists[from_idx][to_idx] + to_dist
    if current_dist >= min_dist:
        return LARGE_INT

    # If loc has a dog, add dog to car
    if to_loc.val >= 20:
        car.append(to_loc.val - 10)

    # If loc has a house, remove dog from car
    if 20 > to_loc.val >= 10:
        car.remove(to_loc.val)

    # If more objects need to be searched
    if len(indices) > 0:

        min_d = LARGE_INT
        for _ in range(len(indices)):
            next_idx = indices.pop(0)
            dist = get_best_dist(to_idx, next_idx, current_dist)
            indices.append(next_idx)
            if dist < min_d:
                min_d = dist
        current_dist = min_d

    # If loc has a dog, remove dog from car
    if to_loc.val >= 20:
        car.remove(to_loc.val - 10)

    # If loc has a house, add dog to car
    if 20 > to_loc.val >= 10:
        car.append(to_loc.val)

    return current_dist


# ---------------------------------------------------------------------------
def find_objects():
    """
    Find all objects in the maze,
    then build table of distances between each pair of objects.
    """

    locs.clear()
    locs.append(car_loc)

    # Find objects in maze
    for y in range(st.grid_size):
        for x in range(st.grid_size):
            value = maze[y][x].val
            if value >= 10:
                locs.append(Loc(x, y, value))

    # Clear distance matrix
    for y in range(17):
        for x in range(17):
            dists[y][x] = 0

    # Get distance between each pair of objects
    for y in range(len(locs)):
        for x in range(y + 1, len(locs)):
            if x != y:
                dists[y][x] = find_shortest_path(locs[y], locs[x])
                dists[x][y] = dists[y][x]


# ---------------------------------------------------------------------------
def find_shortest_path(loc0, loc1):
    """
    Find the shortest path from loc0 to loc1.
    This uses a breadth first search.
    """

    # Clear all visited flags
    for line in maze:
        for cell in line:
            cell.vis = False

    # Mark the cars cell visited and add to queue
    maze[loc0.y][loc0.x].vis = True
    next_cell = [(loc0.x, loc0.y)]

    # While queue not empty,
    # expand search until destination found
    while len(next_cell) > 0:
        x0, y0 = next_cell.pop(0)
        for xy in get_neighbors(x0, y0):
            if xy not in next_cell:
                next_cell.append(xy)
            x, y = xy
            maze[y][x].set(x0, y0)
            if x == loc1.x and y == loc1.y:
                next_cell.clear()
                break

    # Back trace path to get distance
    dist = 0
    x, y, _ = loc1
    while x != loc0.x or y != loc0.y:
        dist += 1
        cell = maze[y][x]
        x = cell.x
        y = cell.y

    return dist


# ---------------------------------------------------------------------------
def get_neighbors(x, y):
    """Make list of neighbors of a cell that have not been visited."""

    neighbors = []

    if maze[y][x].lft and not maze[y][x - 1].vis:
        neighbors.append((x - 1, y))
    if maze[y][x].rit and not maze[y][x + 1].vis:
        neighbors.append((x + 1, y))
    if maze[y][x].top and not maze[y - 1][x].vis:
        neighbors.append((x, y - 1))
    if maze[y][x].bot and not maze[y + 1][x].vis:
        neighbors.append((x, y + 1))

    return neighbors
