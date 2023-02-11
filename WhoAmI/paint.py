# ---------------------------------------------------------------------------
# Who Am I
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame
import state as st

IMAGE_WIDTH = 600
IMAGE_HEIGHT = 600

# Initialize pygame and setup the window
pygame.init()
screen = pygame.display.set_mode((IMAGE_WIDTH, IMAGE_HEIGHT))
pygame.display.set_caption('Who Am I   V1.0')

NAME_FONT = pygame.font.SysFont('Arial', 48)
HEADER_FONT = pygame.font.SysFont('Arial', 60)
INFO_FONT = pygame.font.SysFont('Arial', 26)

CENTER_IMG_LOC = IMAGE_WIDTH // 2, IMAGE_HEIGHT // 3
CENTER_NAME_LOC = IMAGE_WIDTH // 2, 3 * IMAGE_HEIGHT // 4
LEFT_IMG_LOC = IMAGE_WIDTH // 4, IMAGE_HEIGHT // 3
RIGHT_NAME_X = 3 * IMAGE_WIDTH // 5
RIGHT_NAME_Y = 30
RIGHT_NAME_DELTA = 50
STATUS_LOC = 20, IMAGE_HEIGHT - 60

BG_COLOR = 255, 255, 255
WHITE = 255, 255, 255
BLACK = 0, 0, 0
GREEN = 0, 192, 0
GRAY = 192, 192, 192
YELLOW = 255, 255, 0
RED = 255, 0, 0
COLORS = RED, YELLOW, GREEN

STAT0_LOC = 200, 520
STAT1_LOC = 200, 560


# ---------------------------------------------------------------------------
def paint():
    """Paint the screen."""

    screen.fill(WHITE)
    match st.state:
        case st.ST_INTRO: paint_intro()
        case st.ST_SHOW: paint_show()
        case st.ST_WAIT: paint_wait()

    pygame.display.update()


# ---------------------------------------------------------------------------
def paint_status(count):

    screen.fill(BG_COLOR)

    if count > 0:
        text = HEADER_FONT.render(str(count), True, BLACK)
        rect = text.get_rect()
        rect.center = IMAGE_WIDTH // 2, IMAGE_HEIGHT // 2
        screen.blit(text, rect)

    text = f'Round {st.cycle}    Score {st.score} of {st.total}'\
           f'    Level {st.level}'
    text = INFO_FONT.render(text, True, BLACK)
    screen.blit(text, STATUS_LOC)

    pygame.display.update()


# ---------------------------------------------------------------------------
def paint_wait():

    rect = st.image.get_rect()
    rect.center = LEFT_IMG_LOC
    screen.blit(st.image, rect)

    y = RIGHT_NAME_Y
    for _, name in st.names:
        text = NAME_FONT.render(name, True, BLACK)
        screen.blit(text, (RIGHT_NAME_X, y))
        y += RIGHT_NAME_DELTA


# ---------------------------------------------------------------------------
def paint_show():

    rect = st.image.get_rect()
    rect.center = CENTER_IMG_LOC
    screen.blit(st.image, rect)

    text = HEADER_FONT.render(st.name, True, BLACK)
    rect = text.get_rect()
    rect.center = CENTER_NAME_LOC
    screen.blit(text, rect)


# ---------------------------------------------------------------------------
def get_name_idx(xy):
    """Convert from screen coordinates to grid coordinates."""

    if xy[0] < RIGHT_NAME_X:
        return -1

    return (xy[1] - RIGHT_NAME_Y) // RIGHT_NAME_DELTA


# ---------------------------------------------------------------------------
def paint_intro():
    """Paint the intro text screen."""

    intro = (
        '',
        'Click here to start.',
    )

    # Paint the game title
    text = HEADER_FONT.render('Tile Match', True, BLACK)
    rect = text.get_rect()
    rect.center = IMAGE_WIDTH // 2, 40
    screen.blit(text, rect)

    # Paint each line ot intro text
    y = 100
    for line in intro:
        text = INFO_FONT.render(line, True, BLACK)
        rect = text.get_rect()
        rect.center = (IMAGE_WIDTH // 2, y)
        screen.blit(text, rect)
        y += 50
