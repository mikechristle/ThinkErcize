# ---------------------------------------------------------------------------
# Maze Escape
# Paint the screen
# Mike Christle 2023
# ---------------------------------------------------------------------------

import pygame
import state as st


VIEW_HEIGHT = 450
VIEW_WIDTH = 800
VIEW_HALF_HEIGHT = VIEW_HEIGHT // 2

CEILING = 0, 0, VIEW_WIDTH, VIEW_HALF_HEIGHT
FLOOR = 0, VIEW_HALF_HEIGHT, VIEW_WIDTH, VIEW_HALF_HEIGHT

walls = [(0, 0)] * VIEW_WIDTH

# Initialize pygame and setup the window
pygame.init()
pygame.display.set_caption("Maze Escape   V1.0")

screen = pygame.display.set_mode((VIEW_WIDTH, VIEW_HEIGHT))
view_image = pygame.Surface((VIEW_WIDTH, VIEW_HEIGHT))

HEADER_FONT = pygame.font.SysFont('Arial', 64)
INFO_FONT = pygame.font.SysFont('Arial', 36)

BLACK = 0, 0, 0
FLOOR_COLOR = 80, 80, 80
CEILING_COLOR = 160, 160, 160
BLUE0 = 0, 255, 255
BLUE1 = 0, 200, 200
RED0 = 255, 0, 0
RED1 = 200, 0, 0
GREEN0 = 0, 255, 0
GREEN1 = 0, 200, 0

COLORS = [GREEN0, GREEN1, BLUE0, BLUE1, RED1, RED0]


# ---------------------------------------------------------------------------
def paint():
    """Paint the screen."""

    paint_walls()
    if st.game_active:
        screen.blit(view_image, (0, 0))
    else:
        screen.fill(RED1)
        paint_game_over()
    pygame.display.update()


# ---------------------------------------------------------------------------
def paint_walls():
    """Paint the 3D walls."""

    pygame.draw.rect(view_image, FLOOR_COLOR, FLOOR)
    pygame.draw.rect(view_image, CEILING_COLOR, CEILING)
    for x, y in enumerate(walls):
        height, side = y
        height //= 2
        start = x, VIEW_HALF_HEIGHT - height
        stop = x, VIEW_HALF_HEIGHT + height
        color = COLORS[side]
        pygame.draw.line(view_image, color, start, stop)


# ---------------------------------------------------------------------------
def paint_intro():
    """Paint the intro text screen."""

    intro = (
        "In this game you must find you way out of the maze.",
        "The exit door is bright red. The Up and Down arrow",
        "keys will move you forward and backward. The Right",
        "and Left arrow keys will turn 45 degrees right or left.",
        "",
        "Press space bar to start."
    )

    screen.fill(BLACK)

    # Paint the game title
    text = HEADER_FONT.render("Maze Escape", True, BLUE0)
    rect = text.get_rect()
    rect.center = (VIEW_WIDTH // 2, 40)
    screen.blit(text, rect)

    # Paint each line ot intro text
    y = 150
    for line in intro:
        text = INFO_FONT.render(line, True, BLUE0)
        rect = text.get_rect()
        rect.center = (VIEW_WIDTH // 2, y)
        screen.blit(text, rect)
        y += 50

    pygame.display.update()


# ---------------------------------------------------------------------------
def paint_game_over():
    """Paint the game over message."""

    intro = (
        "Congratulations!",
        "You found the exit.",
        f"Your time, {st.run_time:.0f} seconds.",
        "",
        "Press space bar to start a new game."
    )

    y = 150
    for line in intro:
        text = INFO_FONT.render(line, True, GREEN0)
        rect = text.get_rect()
        rect.center = (VIEW_WIDTH // 2, y)
        screen.blit(text, rect)
        y += 50
