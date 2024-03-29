# ---------------------------------------------------------------------------
# Best Route
# Mike Christle 2022
# ---------------------------------------------------------------------------

import state as st

from random import randrange

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ST_IDLE = 0
ST_NEIGHBOR = 1
ST_IN_MAZE = 2
EXTRAS = 0, 0, 0, 0, 2, 3, 4, 5, 6

# ---------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------
last_x = 0
last_y = 0
border_cells = []
maze = [[]]


# ---------------------------------------------------------------------------
def make_maze(size, empty_maze):
    """Build a maze using Prims algorithm."""

    global last_x, last_y, maze

    # Clear the maze
    maze = empty_maze
    for y in range(8):
        for x in range(8):
            st.maze[y][x].clear(x, y)

    cnt_y = size
    cnt_x = size
    last_x = cnt_x - 1
    last_y = cnt_y - 1

    # Pick a random cell to start with
    first_x = randrange(0, cnt_x)
    first_y = randrange(0, cnt_y)
    maze[first_y][first_x].val = ST_IN_MAZE
    border_cells.extend(get_neighbors(first_x, first_y, ST_IDLE, ST_NEIGHBOR))

    while True:

        # Done when there are no more border cells
        cnt = len(border_cells)
        if cnt == 0:
            break

        # Pick a random border cell
        new_cell = border_cells.pop(randrange(cnt))

        # Get the neighbors of the new cell
        n = get_neighbors(new_cell.x, new_cell.y, ST_IN_MAZE, ST_IN_MAZE)

        # If there are no neighbors, the maze os complete
        if len(n) == 0:
            break

        # Pick a random neighbor cell
        old_cell = n.pop(randrange(len(n)))

        # Remove the wall between the cells
        merge_cells(old_cell, new_cell)

        # Find the new neighbors
        n = get_neighbors(new_cell.x, new_cell.y, ST_IDLE, ST_NEIGHBOR)
        border_cells.extend(n)

    # Remove more walls to create loops in maze
    for _ in range(EXTRAS[size]):
        remove_wall(size)

    # Clear all values
    for line in maze:
        for cell in line:
            cell.val = 0


# ---------------------------------------------------------------------------
def get_neighbors(x, y, old_state, new_state):
    """Build a list of all valid neighbors of a given cell."""

    neighbors = []

    # Check the left cell
    if x > 0:
        cell = maze[y][x - 1]
        if cell.val == old_state:
            neighbors.append(cell)
            cell.val = new_state

    # Check the top cell
    if y > 0:
        cell = maze[y - 1][x]
        if cell.val == old_state:
            neighbors.append(cell)
            cell.val = new_state

    # Check the right cell
    if x < last_x:
        cell = maze[y][x + 1]
        if cell.val == old_state:
            neighbors.append(cell)
            cell.val = new_state

    # Check the bottom cell
    if y < last_y:
        cell = maze[y + 1][x]
        if cell.val == old_state:
            neighbors.append(cell)
            cell.val = new_state

    return neighbors


# ---------------------------------------------------------------------------
def merge_cells(cell1, cell2):
    """Remove the wall between two cells."""

    cell1.val = ST_IN_MAZE
    cell2.val = ST_IN_MAZE

    if cell1.x == cell2.x:
        if cell1.y > cell2.y: # cell1 below cell2
            cell1.top = True
            cell2.bot = True
        else:                 # cell1 above cell2
            cell1.bot = True
            cell2.top = True
    else:
        if cell1.x > cell2.x: # cell1 right of cell2
            cell1.lft = True
            cell2.rit = True
        else:                 # cell1 left of cell2
            cell1.rit = True
            cell2.lft = True


# ---------------------------------------------------------------------------
def remove_wall(size):
    """Pick a random cell in the given region and remove a wall."""

    max_xy = size - 1

    while True:

        # Pick a random cell
        x = randrange(size)
        y = randrange(size)
        cell = maze[y][x]

        # Pick a random direction
        match randrange(4):

            # If cell has a right wall, remove it
            case 0 if not cell.rit and x < max_xy:
                cell.rit = True
                maze[y][x + 1].lft = True
                break

            # If cell has a left wall, remove it
            case 1 if not cell.lft and x > 0:
                cell.lft = True
                maze[y][x - 1].rit = True
                break

            # If cell has a top wall, remove it
            case 2 if not cell.top and y > 0:
                cell.top = True
                maze[y - 1][x].bot = True
                break

            # If cell has a bottom wall, remove it
            case 3 if not cell.bot and y < max_xy:
                cell.bot = True
                maze[y + 1][x].top = True
                break
