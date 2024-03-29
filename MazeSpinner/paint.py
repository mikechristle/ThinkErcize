# ---------------------------------------------------------------------------
# Maze Spinner
# Paint the screen
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame as pg
import state as st

from math import sqrt

CELL_SIZE = 36
BALL_SIZE = CELL_SIZE - 6

IMAGE_SIZE = (st.MAZE_SIZE + 2) * CELL_SIZE
SCREEN_SIZE = int(sqrt(IMAGE_SIZE * IMAGE_SIZE * 2))
IMAGE_CENTER = SCREEN_SIZE // 2, SCREEN_SIZE // 2

# Initialize pygame and setup the window
pg.init()
screen = pg.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pg.display.set_caption("Maze Spinner   V1.1")
maze_image = pg.Surface((IMAGE_SIZE, IMAGE_SIZE))

HEADER_FONT = pg.font.SysFont('Arial', 64)
INFO_FONT = pg.font.SysFont('Arial', 36)

WHITE = 255, 255, 255
BLACK = 0, 0, 0
BLUE = 0, 0, 255
RED = 255, 0, 0
GREEN = 0, 200, 0

# Used by the draw_arrow function
X1 = 0
X2 = CELL_SIZE // 2
X3 = CELL_SIZE
Y1 = CELL_SIZE * 3
Y2 = Y1 + CELL_SIZE
Y3 = (st.MAZE_SIZE - 1) * CELL_SIZE


# ---------------------------------------------------------------------------
def paint():
    """Paint the screen."""

    screen.fill(WHITE)

    x = ((st.ball_x + 1) * CELL_SIZE) + 3
    y = ((st.ball_y + 1) * CELL_SIZE) + 3
    ball_rect = pg.Rect(x, y, BALL_SIZE, BALL_SIZE)
    pg.draw.ellipse(maze_image, RED, ball_rect)

    rotated_image = pg.transform.rotate(maze_image, st.rotation_angle)
    img_rect = rotated_image.get_rect()
    img_rect.center = IMAGE_CENTER
    screen.blit(rotated_image, img_rect)

    paint_status()
    pg.display.update()

    pg.draw.ellipse(maze_image, WHITE, ball_rect)


# ---------------------------------------------------------------------------
def init_maze_image():
    """Paint the maze."""

    maze_image.fill(WHITE)

    # For each cell in maze
    for y in range(st.MAZE_SIZE):
        for x in range(st.MAZE_SIZE):
            cell = st.maze[y][x]

            # Coordinates of upper left corner
            x0 = (x + 1) * CELL_SIZE
            y0 = (y + 1) * CELL_SIZE
            p1 = x0, y0

            # Draw left side wall
            if not cell.lft:
                p2 = x0, y0 + CELL_SIZE
                pg.draw.line(maze_image, BLACK, p1, p2, width=3)

            # Draw top side wall
            if not cell.top:
                p2 = x0 + CELL_SIZE, y0
                pg.draw.line(maze_image, BLACK, p1, p2, width=3)

    # Draw walls on right and bottom sides of maze
    x0 = (st.MAZE_SIZE + 1) * CELL_SIZE
    p1 = x0, x0
    p2 = CELL_SIZE, x0
    pg.draw.line(maze_image, BLACK, p1, p2, width=3)
    p2 = x0, CELL_SIZE
    pg.draw.line(maze_image, BLACK, p1, p2, width=3)
    draw_arrow(0)
    draw_arrow((st.MAZE_SIZE + 1) * CELL_SIZE)

    # Draw a blue ball to mark the exit
    x = (st.MAZE_SIZE * CELL_SIZE) + 3
    y = (st.MAZE_SIZE * CELL_SIZE) + 3
    ball_rect = pg.Rect(x, y, BALL_SIZE, BALL_SIZE)
    pg.draw.ellipse(maze_image, BLUE, ball_rect)


# ---------------------------------------------------------------------------
def draw_arrow(offset):
    """Draw the red arrow on each side of the maze."""

    p1 = X2 + offset, Y1
    p2 = X2 + offset, Y3
    pg.draw.line(maze_image, RED, p1, p2, width=5)
    p1 = X2 + offset, Y1
    p2 = X1 + offset, Y2
    p3 = X3 + offset, Y2
    pg.draw.polygon(maze_image, RED, (p1, p2, p3), width=0)


# ---------------------------------------------------------------------------
def paint_status():
    """Paint the status bar."""

    if not st.game_active:
        text = f'Time {st.elapsed_time:.2f} Seconds'\
               '       Press space bar to start'
        text = INFO_FONT.render(text, True, BLUE)
        screen.blit(text, (15, SCREEN_SIZE - 50))


# ---------------------------------------------------------------------------
def paint_intro():
    """Paint the intro text screen."""

    intro = (
        "In this game you must navigate the red dot",
        "out of the maze, as fast as you can,",
        "using the keyboard arrow keys.",
        "The exit is at the lower right-hand corner,",
        "marked by the blue dot.",
        "The red arrows on either side of the maze",
        "will help you keep track of which way is",
        "up as the maze rotates.",
        "",
        "Press space bar to start."
    )

    screen.fill(WHITE)

    # Paint the game title
    text = HEADER_FONT.render("Maze Spinner", True, BLUE)
    rect = text.get_rect()
    rect.center = (SCREEN_SIZE // 2, 40)
    screen.blit(text, rect)

    # Paint each line ot intro text
    y = 150
    for line in intro:
        text = INFO_FONT.render(line, True, BLUE)
        rect = text.get_rect()
        rect.center = (SCREEN_SIZE // 2, y)
        screen.blit(text, rect)
        y += 50

    pg.display.update()
