# ---------------------------------------------------------------------------
# Memory Patterns
# Paint the screen
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame as pg
import state as st

CELL_SIZE = 60
BG_SIZE = 8 * CELL_SIZE
IMAGE_WIDTH = BG_SIZE
IMAGE_HEIGHT = BG_SIZE + CELL_SIZE
STATUS_LOC = (0, BG_SIZE + 10)
TILE_SIZE = CELL_SIZE - 7

# Initialize pygame and setup the window
pg.init()
screen = pg.display.set_mode((IMAGE_WIDTH, IMAGE_HEIGHT))
pg.display.set_caption('Memory Patterns   V1.2')

bg_image = pg.Surface((BG_SIZE, BG_SIZE))
offset_x = 0
offset_y = 0

HEADER_FONT = pg.font.SysFont('Arial', 48)
INFO_FONT = pg.font.SysFont('Arial', 32)
STATUS_FONT = pg.font.SysFont('Arial', 26)

BG_COLOR = 255, 255, 255
WHITE = 255, 255, 255
BLACK = 0, 0, 0
GREEN = 0, 127, 0
GRAY = 127, 127, 127
RED = 255, 0, 0
COLORS = (
    (WHITE, GREEN, GRAY, RED), # state = INTRO
    (WHITE, GREEN, GRAY, RED), # state = COUNT
    (WHITE, WHITE, GRAY, RED), # state = WAIT
    (WHITE, GREEN, GRAY, RED),  # state = SHOW
)


# ---------------------------------------------------------------------------
def paint():
    """Paint the screen."""

    screen.fill(BG_COLOR)
    screen.blit(bg_image, (0, 0))
    paint_pattern()
    paint_status()
    pg.display.update()


# ---------------------------------------------------------------------------
def paint_count(count):
    """Paint the counter."""

    screen.fill(BG_COLOR)
    text = HEADER_FONT.render(count, True, BLACK)
    rect = text.get_rect()
    rect.center = IMAGE_WIDTH // 2, IMAGE_HEIGHT // 2
    screen.blit(text, rect)
    pg.display.update()


# ---------------------------------------------------------------------------
def paint_pattern():
    """Paint the cells of the grid."""

    # For each cell in the grid
    width, height, _ = st.LEVELS[st.level]
    for y in range(7):
        y0 = (y * CELL_SIZE) + offset_y + 4
        for x in range(7):
            x0 = (x * CELL_SIZE) + offset_x + 4
            cell = st.grid[y][x]

            # If cell is not blank, fill with a color
            if cell != st.BLANK:
                color = COLORS[st.state][cell]
                rect = x0, y0, TILE_SIZE, TILE_SIZE
                pg.draw.rect(screen, color, rect)


# ---------------------------------------------------------------------------
def paint_background():
    """Paint the grid outline."""

    global offset_x, offset_y

    # Get the dimensions of the grid
    width, height, _ = st.LEVELS[st.level]

    # Set the offset from the left edge of screen to
    # left edge of grid
    offset_x = (8 - width) * CELL_SIZE // 2
    offset_y = (8 - height) * CELL_SIZE // 2

    # Set the offset to the right edge of grid
    right = offset_x + (width * CELL_SIZE)
    bottom = offset_y + (height * CELL_SIZE)

    # Clear the previous grid
    bg_image.fill(BG_COLOR)

    # Draw the vertical lines
    for x in range(width + 1):
        p0 = offset_x + (x * CELL_SIZE), offset_y
        p1 = offset_x + (x * CELL_SIZE), bottom
        pg.draw.line(bg_image, BLACK, p0, p1, width=3)

    # Draw the horizontal lines
    for y in range(height + 1):
        p0 = offset_x, offset_y + (y * CELL_SIZE)
        p1 = right, offset_y + (y * CELL_SIZE)
        pg.draw.line(bg_image, BLACK, p0, p1, width=3)


# ---------------------------------------------------------------------------
def paint_status():
    """Paint the status bar."""

    if st.state == st.ST_COUNT:
        return

    if st.state == st.ST_WAIT:
        text = f'  Click the squares that were green'
    else:
        text = f'  Round {st.cycle}   Score {st.score}'
    if st.state == st.ST_INTRO:
        text += '     Click to start new game'
    text = STATUS_FONT.render(text, True, BLACK)
    screen.blit(text, STATUS_LOC)


# ---------------------------------------------------------------------------
def get_xy(xy):
    """Convert screen coordinates to grid coordinates."""

    x = (xy[0] - offset_x) // CELL_SIZE
    y = (xy[1] - offset_y) // CELL_SIZE
    return x, y


# ---------------------------------------------------------------------------
def paint_intro():
    """Paint the intro text screen."""

    intro = (
        'The purpose of this game is to',
        'exercise your ability to remember a',
        'visual pattern. A random pattern of',
        'squares will briefly appear.',
        'Then you click on the squares that',
        'were highlighted. Get all squares',
        'to advance to next level.',
        '',
        'Click here to start.',
    )

    # Paint the game title
    screen.fill(BG_COLOR)
    text = HEADER_FONT.render('Memory Patterns', True, BLACK)
    rect = text.get_rect()
    rect.center = (IMAGE_WIDTH // 2, 40)
    screen.blit(text, rect)

    # Paint each line ot intro text
    y = 100
    for line in intro:
        text = INFO_FONT.render(line, True, BLACK)
        rect = text.get_rect()
        rect.center = (IMAGE_WIDTH // 2, y)
        screen.blit(text, rect)
        y += 40

    pg.display.update()
