# ---------------------------------------------------------------------------
# Digit Order
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame
import state as st

CELL_SIZE = 50
STATUS_HEIGHT = 40
IMAGE_WIDTH = st.GRID_WIDTH * CELL_SIZE
IMAGE_HEIGHT = st.GRID_HEIGHT * CELL_SIZE

COUNT_X = (IMAGE_WIDTH - CELL_SIZE) // 2
COUNT_Y = (IMAGE_HEIGHT - CELL_SIZE) // 2
COUNT_RECT = COUNT_X, COUNT_Y, CELL_SIZE, CELL_SIZE
COUNT_LOC = COUNT_X + 20, COUNT_Y + 8

# Initialize pygame and setup the window
pygame.init()
screen = pygame.display.set_mode((IMAGE_WIDTH, IMAGE_HEIGHT + STATUS_HEIGHT))
pygame.display.set_caption('Digit Order   V1.0')

HEADER_FONT = pygame.font.SysFont('Arial', 52)
TEXT_FONT = pygame.font.SysFont('Arial', 30)
NUMBER_FONT = pygame.font.SysFont('Arial', 32)
STATUS_FONT = pygame.font.SysFont('Arial', 30)

BG_COLOR = 107, 142, 35
WHITE = 255, 255, 255
YELLOW = 255, 255, 0
BLACK = 0, 0, 0
GREEN = 0, 255, 0
RED = 255, 0, 0
COLORS = (None, GREEN, GREEN, RED)


# ---------------------------------------------------------------------------
def paint():
    """Paint the screen."""

    screen.fill(BG_COLOR)
    paint_grid()
    paint_status()
    pygame.display.update()


# ---------------------------------------------------------------------------
def paint_grid():
    """Paint the numbers and circles."""

    for y in range(st.GRID_HEIGHT):
        for x in range(st.GRID_WIDTH):
            cell = st.grid[y][x]
            if cell.state == st.BLANK:
                continue
            if st.state == st.ST_WAIT and cell.state == st.NUMBER:
                paint_circle(x, y, GREEN)
            else:
                paint_number(x, y, cell.value)
                paint_circle(x, y, COLORS[cell.state])


# ---------------------------------------------------------------------------
def paint_circle(x, y, color):
    """Paint a circle."""

    rect = x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE
    pygame.draw.ellipse(screen, color, rect, width=5)


# ---------------------------------------------------------------------------
def paint_number(x, y, number):
    """Paint a number."""

    text = str(number)
    text = NUMBER_FONT.render(text, True, WHITE)
    loc = (x * CELL_SIZE) + 18, (y * CELL_SIZE) + 6
    screen.blit(text, loc)


# ---------------------------------------------------------------------------
def paint_count(count):
    """Paint the count down counter."""

    screen.fill(BG_COLOR)
    text = HEADER_FONT.render(count, True, YELLOW)
    rect = text.get_rect()
    rect.center = IMAGE_WIDTH // 2, IMAGE_HEIGHT // 2
    screen.blit(text, rect)
    pygame.display.update()


# ---------------------------------------------------------------------------
def paint_status():
    """Paint the contents of the status bar."""

    text = f'   Score {st.score}   '\
           f'Round {st.cycle}'
    if st.state == st.ST_IDLE:
        text += '    Click to start game'
    text = STATUS_FONT.render(text, True, WHITE)
    screen.blit(text, (0, IMAGE_HEIGHT + 6))


# ---------------------------------------------------------------------------
def get_xy(xy):
    """Convert from screen coordinates to grid coordinates."""

    return xy[0] // CELL_SIZE, xy[1] // CELL_SIZE


# ---------------------------------------------------------------------------
def show_intro():
    """Paint the intro text screen."""

    intro = (
        'This game will help you to focus on and',
        'remember details. A series of circles',
        'will appear on the screen. Each circle',
        'will briefly display a digit from 1 to 9.',
        'After the digits disappear you must',
        'click the mouse on each circle in order',
        'from lowest digit to highest. For each',
        'correct click you earn one point.',
        'A game consist of 10 rounds.',
        'Click to start game.',
    )

    # Paint the game title
    screen.fill(BG_COLOR)
    text = HEADER_FONT.render('Digit Order', True, WHITE)
    rect = text.get_rect()
    rect.center = (IMAGE_WIDTH // 2, 30)
    screen.blit(text, rect)

    # Paint each line ot intro text
    y = 80
    for line in intro:
        text = TEXT_FONT.render(line, True, WHITE)
        rect = text.get_rect()
        rect.center = (IMAGE_WIDTH // 2, y)
        screen.blit(text, rect)
        y += 35

    pygame.display.update()
