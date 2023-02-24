# ---------------------------------------------------------------------------
# Maze Spinner
# A game to enhance your speed and concentration.
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame as pg
import state as st

from time import time
from random import randrange, choice
from sys import exit
from make_maze import make_maze
from paint import paint, paint_intro, init_maze_image

pg.time.set_timer(pg.USEREVENT, 1000)

angle = 0.0
count = 0
start_time = 0.0

EXIT_X = st.MAZE_SIZE - 1
EXIT_Y = st.MAZE_SIZE - 1


# ---------------------------------------------------------------------------
def main():
    """Main routine."""

    # Display the intro screen
    paint_intro()

    while True:

        # Get all pygame events
        for event in pg.event.get():
            match event.type:

                # Exit if window is closed
                case pg.QUIT:
                    exit()

                # Start a new game when space bar is pressed
                case pg.KEYDOWN if not st.game_active:
                    if event.key == pg.K_SPACE:
                        make_maze()
                        init_maze_image()
                        start_game()
                        paint()

                # Press arrow keys to move ball
                case pg.KEYDOWN if st.game_active:
                    move_ball(event.key)
                    paint()

                # One second timer event to rotate maze
                case pg.USEREVENT if st.game_active:
                    rotate_maze()
                    paint()


# ---------------------------------------------------------------------------
def rotate_maze():
    """One second timer event to rotate maze."""

    global count, angle

    if count > 0:
        st.rotation_angle += angle
        count -= 1
    else:
        angle = choice((20.0, -20.0))
        count = randrange(2, 10)


# ---------------------------------------------------------------------------
def move_ball(key):
    """Move the ball in response to arrow keys."""

    cell = st.maze[st.ball_y][st.ball_x]

    if key == pg.K_UP and cell.top:
        st.ball_y -= 1
    elif key == pg.K_DOWN and cell.bot:
        st.ball_y += 1
    elif key == pg.K_RIGHT and cell.rit:
        st.ball_x += 1
    elif key == pg.K_LEFT and cell.lft:
        st.ball_x -= 1

    # Check for ball at exit cell
    if st.ball_y == EXIT_Y and st.ball_x == EXIT_X:
        st.game_active = False
        end_time = time()
        st.elapsed_time = end_time - start_time


# ---------------------------------------------------------------------------
def start_game():
    """Setup for a new game."""

    global start_time, angle, count

    st.ball_x = 0
    st.ball_y = 0
    st.game_active = True
    st.rotation_angle = 0.0
    angle = 20.0
    count = 5
    start_time = time()


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
