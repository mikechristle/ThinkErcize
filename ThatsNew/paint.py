# ---------------------------------------------------------------------------
# Laser Path
# Paint the screen
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame
import state

from images import IMAGES

CELL_SIZE = 60
PAD = (CELL_SIZE - 48) // 2

IMAGE_WIDTH = 8 * CELL_SIZE
IMAGE_HEIGHT = 7 * CELL_SIZE

STATUS_HEIGHT = CELL_SIZE
STATUS_LOC = IMAGE_WIDTH // 2, int(6.5 * CELL_SIZE)

# Initialize pygame and setup the window
pygame.init()
screen = pygame.display.set_mode((IMAGE_WIDTH, IMAGE_HEIGHT))
pygame.display.set_caption("What's New   V1.0")

HEADER_FONT = pygame.font.SysFont('Arial', 64)
INFO_FONT = pygame.font.SysFont('Arial', 32)

WHITE = 255, 255, 255
BLACK = 0, 0, 0
BLUE = 0, 0, 255
RED = 255, 0, 0
GREEN = 0, 200, 0
BG_COLORS = (WHITE, GREEN, WHITE, RED)


# ---------------------------------------------------------------------------
def paint():
    """Paint the screen."""

    screen.fill(WHITE)
    paint_grid()
    paint_status()
    pygame.display.update()


# ---------------------------------------------------------------------------
def paint_grid():
    """Paint images on the grid."""

    for y in range(6):
        for x in range(8):
            img, bg = state.grid[y][x]

            # If game is over, paint borders to indicate image status
            if not state.game_active and img > 0:
                color = BG_COLORS[bg]
                rect = x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE
                pygame.draw.rect(screen, color, rect)

            # Paint images
            if img > 0:
                img = IMAGES[img - 1]
                loc = (x * CELL_SIZE) + PAD, (y * CELL_SIZE) + PAD
                screen.blit(img, loc)


# ---------------------------------------------------------------------------
def paint_status():
    """Paint the status bar."""

    if not state.game_active:
        text = 'Click here to start a new game.'
        text = INFO_FONT.render(text, True, BLUE)
        rect = text.get_rect()
        rect.center = STATUS_LOC
        screen.blit(text, rect)


# ---------------------------------------------------------------------------
def get_xy(xy):
    """Convert screen coordinates to grid coordinates."""

    return xy[0] // CELL_SIZE, xy[1] // CELL_SIZE


# ---------------------------------------------------------------------------
def paint_intro():
    """Paint the intro text screen."""

    intro = (
        "Can you remember which objects",
        "you have seen before.",
        "Click on a new object.",
        "",
        "Click here to start."
    )

    screen.fill(WHITE)

    # Paint the game title
    text = HEADER_FONT.render("That's New", True, BLUE)
    rect = text.get_rect()
    rect.center = (IMAGE_WIDTH // 2, 40)
    screen.blit(text, rect)

    # Paint each line ot intro text
    y = 120
    for line in intro:
        text = INFO_FONT.render(line, True, BLUE)
        rect = text.get_rect()
        rect.center = (IMAGE_WIDTH // 2, y)
        screen.blit(text, rect)
        y += 60

    pygame.display.update()
