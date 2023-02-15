# ---------------------------------------------------------------------------
# Best Route
# Mike Christle 2022
# ---------------------------------------------------------------------------

import state as st

from make_maze import make_maze
from random import randrange
from time import sleep
from paint import paint

path = []


# ---------------------------------------------------------------------------
def start_game():
    """Initialize the game board to start a game."""

    make_maze(st.grid_size, st.maze)
    st.miles = 0

    # Add houses to maze
    count = st.level
    st.house_count = count
    while count > 0:
        x = randrange(st.grid_size)
        y = randrange(st.grid_size)
        cell = st.maze[y][x]
        if cell.val == 0:
            cell.val = 9 + count
            count -= 1

    # Add dogs to maze
    count = st.level
    while count > 0:
        x = randrange(st.grid_size)
        y = randrange(st.grid_size)
        cell = st.maze[y][x]
        if cell.val == 0:
            cell.val = 19 + count
            count -= 1

    # Add players car to maze
    while True:
        st.car_x = randrange(st.grid_size)
        st.car_y = randrange(st.grid_size)
        cell = st.maze[st.car_y][st.car_x]
        if cell.val == 0:
            cell.val = 1
            break


# ---------------------------------------------------------------------------
def click(x, y):
    """Process clicks on the game board."""

    # Ignore clicks outside of the game board
    if x < 0 or x >= st.grid_size or y < 0 or y >= st.grid_size:
        return

    # Ignore cells that do not have a dog or a house
    cell = st.maze[y][x]
    if cell.val < 10:
        return

    # Clicked on a dog
    if cell.val >= 20:
        if len(st.car) < 3:
            dog = cell.val
            find_shortest_path(x, y)
            move_car(x, y)
            st.car.append(dog)

    # Clicked on a house
    elif cell.val >= 10:
        dog = cell.val + 10
        if dog in st.car:
            find_shortest_path(x, y)
            move_car(x, y)
            st.car.remove(dog)
            st.house_count -= 1
            if st.house_count == 0:
                st.state = st.ST_IDLE


# ---------------------------------------------------------------------------
def move_car(x, y):
    """Animation to move car to a new cell."""

    st.maze[st.car_y][st.car_x].val = 0
    while len(path) > 0:
        st.miles += 1
        sleep(0.3)
        x, y = path.pop(0)
        hold = st.maze[y][x].val
        st.maze[y][x].val = 1
        paint()
        st.maze[y][x].val = hold

    st.car_x = x
    st.car_y = y
    st.maze[st.car_y][st.car_x].val = 1


# ---------------------------------------------------------------------------
def find_shortest_path(dest_x, dest_y):
    """
    Find the shortest path from car to destination.
    This uses a breadth first search.
    """

    # Clear all visited flags
    for line in st.maze:
        for cell in line:
            cell.vis = False

    # Mark the cars cell visited and add to queue
    st.maze[st.car_y][st.car_x].vis = True
    next_cell = [(st.car_x, st.car_y)]

    # While queue not empty,
    # expand search until destination found
    while len(next_cell) > 0:
        x0, y0 = next_cell.pop(0)
        for x, y in get_neighbors(x0, y0):
            next_cell.append((x, y))
            cell = st.maze[y][x]
            cell.x = x0
            cell.y = y0
            cell.vis = True
            if x == dest_x and y == dest_y:
                next_cell.clear()
                break

    # Walk back through the maze to assemble the path
    x, y = dest_x, dest_y
    while x != st.car_x or y != st.car_y:
        path.append((x, y))
        cell = st.maze[y][x]
        x = cell.x
        y = cell.y
    path.reverse()


# ---------------------------------------------------------------------------
def get_neighbors(x, y):
    """Make list of neighbors of a cell that have not been visited."""

    neighbors = []

    if st.maze[y][x].lft and not st.maze[y][x - 1].vis:
        neighbors.append((x - 1, y))
    if st.maze[y][x].rit and not st.maze[y][x + 1].vis:
        neighbors.append((x + 1, y))
    if st.maze[y][x].top and not st.maze[y - 1][x].vis:
        neighbors.append((x, y - 1))
    if st.maze[y][x].bot and not st.maze[y + 1][x].vis:
        neighbors.append((x, y + 1))

    return neighbors
