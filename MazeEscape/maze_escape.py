# ---------------------------------------------------------------------------
# Maze Escape
# Mike Christle 2023
# ---------------------------------------------------------------------------

import pygame as pg
import state as st

from random import randrange
from sys import exit
from make_maze import make_maze
from paint import paint, paint_intro
from view_3d import make_3d_view
from time import time

EMPTY = 0
BORDER_WALL = 1
INTERNAL_WALL = 2
EXIT_DOOR = 3
GRID_MAX = st.GRID_SIZE - 1


# ---------------------------------------------------------------------------
def main():
    """Main routine."""

    # st.game_active = False
    paint_intro()
    while True:

        # Get all pygame events
        for event in pg.event.get():
            match [event.type, st.game_active]:

                # Exit if window is closed
                case [pg.QUIT, _]:
                    exit()

                # Space bar start a game
                case [pg.KEYDOWN, False]:
                    if event.key == pg.K_SPACE:
                        make_maze()
                        fill_grid()
                        make_3d_view()
                        paint()
                        st.run_time = time()

                # Arrow keys move the player
                case [pg.KEYDOWN, True]:
                    move_player(event.key)
                    make_3d_view()
                    paint()


# ---------------------------------------------------------------------------
def move_player(key):
    """Decode arrow keys and move the player."""

    # Right arrow rotates 45 degrees right
    if key == pg.K_RIGHT:
        st.angle = (st.angle - 1) & 7
        return

    # Left arrow rotates 45 degrees left
    if key == pg.K_LEFT:
        st.angle = (st.angle + 1) & 7
        return

    # Down key moves player backward
    x, y, a = st.pos_x, st.pos_y, st.angle
    if key == pg.K_DOWN:
        a = (a + 4) & 7
        key = pg.K_UP

    # Up key moves player forward
    if key == pg.K_UP:

        # Decode the angle to get x y deltas
        match a:
            case 0:
                x += 1
            case 1:
                x += 1
                y -= 1
            case 2:
                y -= 1
            case 3:
                x -= 1
                y -= 1
            case 4:
                x -= 1
            case 5:
                x -= 1
                y += 1
            case 6:
                y += 1
            case 7:
                x += 1
                y += 1

    # If the new cell is empty, move to that cell
    cell_state = st.grid[y][x]
    if cell_state == 0:
        st.pos_x, st.pos_y = x, y

    # If the new cell is an exit, end the game
    elif cell_state == 3:
        st.game_active = False
        st.run_time = time() - st.run_time


# ---------------------------------------------------------------------------
def fill_grid():
    """Copy walls from the maze to the view grid."""

    # Position the player in the corner of the maze
    st.game_active = True
    st.pos_x = st.GRID_CELL // 2
    st.pos_y = st.GRID_CELL // 2

    # Clear all walls from previous game
    for y in range(st.GRID_SIZE):
        for x in range(st.GRID_SIZE):
            st.grid[y][x] = EMPTY

    # Fill in the internal walls of the maze
    for y in range(st.MAZE_SIZE):
        y0 = y * st.GRID_CELL
        for x in range(st.MAZE_SIZE):
            x0 = x * st.GRID_CELL
            cell = st.maze[y][x]
            if not cell.lft:
                for y1 in range(y0, y0 + st.GRID_CELL):
                    st.grid[y1][x0] = INTERNAL_WALL
            if not cell.top:
                for x1 in range(x0, x0 + st.GRID_CELL):
                    st.grid[y0][x1] = INTERNAL_WALL
            if cell.lft and cell.top:
                st.grid[y0][x0] = INTERNAL_WALL

    # Fill in the border walls
    for x in range(st.GRID_SIZE):
        st.grid[0][x] = BORDER_WALL
    for y in range(st.GRID_SIZE):
        st.grid[y][0] = BORDER_WALL
    for x in range(st.GRID_SIZE):
        st.grid[GRID_MAX][x] = BORDER_WALL
    for y in range(st.GRID_SIZE):
        st.grid[y][GRID_MAX] = BORDER_WALL

    # Randomly place the exit door
    while True:
        x = randrange(st.GRID_SIZE)
        y = randrange(st.GRID_SIZE)
        if st.grid[y][x] == EMPTY:
            continue

        # Exit must be in a wall next to at least one empty space
        if x > 0 and st.grid[y][x - 1] == EMPTY or \
           y > 0 and st.grid[y - 1][x] == EMPTY or \
           x < GRID_MAX and st.grid[y][x + 1] == EMPTY or \
           y < GRID_MAX and st.grid[y + 1][x] == EMPTY:
                st.grid[y][x] = EXIT_DOOR
                break


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()

