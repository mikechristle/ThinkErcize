# ---------------------------------------------------------------------------
# Maze Spinner
# A game to enhance your speed and concentration.
# Mike Christle 2022
# ---------------------------------------------------------------------------

import sys
import pygame
import state
import random
import time

from make_maze import make_maze
from paint import paint, paint_intro, init_maze_image

pygame.time.set_timer(pygame.USEREVENT, 1000)

angle = 0.0
count = 0
start_time = 0.0

EXIT_X = state.MAZE_SIZE - 1
EXIT_Y = state.MAZE_SIZE - 1


# ---------------------------------------------------------------------------
def main():
    """Main routine."""

    # Display the intro screen
    paint_intro()

    while True:

        # Get all pygame events
        for event in pygame.event.get():
            match event.type:

                # Exit if window is closed
                case pygame.QUIT:
                    sys.exit()

                # Start a new game when space bar is pressed
                case pygame.KEYDOWN if not state.game_active:
                    if event.key == pygame.K_SPACE:
                        make_maze()
                        init_maze_image()
                        start_game()
                        paint()

                # Press arrow keys to move ball
                case pygame.KEYDOWN if state.game_active:
                    move_ball(event.key)
                    paint()

                # One second timer event to rotate maze
                case pygame.USEREVENT if state.game_active:
                    rotate_maze()
                    paint()


# ---------------------------------------------------------------------------
def rotate_maze():
    """One second timer event to rotate maze."""

    global count, angle

    if count > 0:
        state.rotation_angle += angle
        count -= 1
    else:
        angle = random.choice((20.0, -20.0))
        count = random.randrange(2, 10)


# ---------------------------------------------------------------------------
def move_ball(key):
    """Move the ball in response to arrow keys."""

    cell = state.maze[state.ball_y][state.ball_x]

    if key == pygame.K_UP and cell.top:
        state.ball_y -= 1
    elif key == pygame.K_DOWN and cell.bot:
        state.ball_y += 1
    elif key == pygame.K_RIGHT and cell.rit:
        state.ball_x += 1
    elif key == pygame.K_LEFT and cell.lft:
        state.ball_x -= 1

    # Check for ball at exit cell
    if state.ball_y == EXIT_Y and state.ball_x == EXIT_X:
        state.game_active = False
        end_time = time.time()
        state.elapsed_time = end_time - start_time


# ---------------------------------------------------------------------------
def start_game():
    """Setup for a new game."""

    global start_time, angle, count

    state.ball_x = 0
    state.ball_y = 0
    state.game_active = True
    state.rotation_angle = 0.0
    angle = 20.0
    count = 5
    start_time = time.time()


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
