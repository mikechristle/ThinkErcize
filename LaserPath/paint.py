# ---------------------------------------------------------------------------
# Laser Path, Paint
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame
import state as st

from time import sleep

CELL_SIZE = 80
CELL_COUNT = 7

HALF_CELL_SIZE = CELL_SIZE // 2
IMAGE_WIDTH = CELL_COUNT * CELL_SIZE
IMAGE_HEIGHT = CELL_COUNT * CELL_SIZE
STATUS_HEIGHT = CELL_SIZE // 2

# Initialize pygame and setup the window
pygame.init()
screen = pygame.display.set_mode((IMAGE_WIDTH, IMAGE_HEIGHT + STATUS_HEIGHT))
pygame.display.set_caption('Laser Path   V1.2')

bg_image = pygame.Surface((IMAGE_WIDTH, IMAGE_HEIGHT))
st_image = pygame.Surface((IMAGE_WIDTH, STATUS_HEIGHT))
count_image = pygame.Surface((CELL_SIZE // 2, CELL_SIZE // 2))

laser_path = []

HEADER_FONT_SIZE = CELL_SIZE #// 2
INFO_FONT_SIZE = CELL_SIZE // 3
HEADER_FONT = pygame.font.SysFont('Arial', HEADER_FONT_SIZE)
INFO_FONT = pygame.font.SysFont('Arial', INFO_FONT_SIZE)
COUNT_FONT = pygame.font.SysFont('Arial', CELL_SIZE)

BG_COLOR = 107, 142, 35
WHITE = 255, 255, 255
BLACK = 0, 0, 0
GREEN = 0, 127, 0
GRAY = 127, 127, 127
DARK_GRAY = 96, 96, 96
YELLOW = 255, 255, 0
RED = 255, 0, 0


# ---------------------------------------------------------------------------
def paint():
    """Paint the screen."""

    screen.fill(BLACK)
    screen.blit(bg_image, (0, 0))
    screen.blit(st_image, (0, (CELL_SIZE * 7) + 1))

    match st.state:
        case st.ST_SHOW:
            show_mirrors()
        case st.ST_WAIT:
            show_laser()

    pygame.display.update()


# ---------------------------------------------------------------------------
def show_laser():
    """Paint a laser cannon."""

    for y in range(7):
        for x in range(7):

            match st.grid[y][x]:
                case st.EMPTY:
                    continue
                case st.LASER_N:
                    x0 = (x * CELL_SIZE) + 4
                    y0 = (y * CELL_SIZE) + CELL_SIZE
                    x1 = (x * CELL_SIZE) + CELL_SIZE - 4
                    y1 = y0
                    x2 = (x * CELL_SIZE) + HALF_CELL_SIZE
                    y2 = (y * CELL_SIZE) + 4
                    pts = (x0, y0), (x1, y1), (x2, y2)
                    pygame.draw.polygon(screen, RED, pts)
                case st.LASER_S:
                    x0 = (x * CELL_SIZE) + 4
                    y0 = (y * CELL_SIZE)
                    x1 = (x * CELL_SIZE) + CELL_SIZE - 4
                    y1 = y0
                    x2 = (x * CELL_SIZE) + HALF_CELL_SIZE
                    y2 = (y * CELL_SIZE) + CELL_SIZE - 4
                    pts = (x0, y0), (x1, y1), (x2, y2)
                    pygame.draw.polygon(screen, RED, pts)
                case st.LASER_E:
                    x0 = (x * CELL_SIZE)
                    y0 = (y * CELL_SIZE) + 4
                    x1 = x0
                    y1 = (y * CELL_SIZE) + CELL_SIZE - 4
                    x2 = (x * CELL_SIZE) + CELL_SIZE - 4
                    y2 = (y * CELL_SIZE) + HALF_CELL_SIZE
                    pts = (x0, y0), (x1, y1), (x2, y2)
                    pygame.draw.polygon(screen, RED, pts)
                case st.LASER_W:
                    x0 = (x * CELL_SIZE) + CELL_SIZE
                    y0 = (y * CELL_SIZE) + 4
                    x1 = x0
                    y1 = (y * CELL_SIZE) + CELL_SIZE - 4
                    x2 = (x * CELL_SIZE) + 4
                    y2 = (y * CELL_SIZE) + HALF_CELL_SIZE
                    pts = (x0, y0), (x1, y1), (x2, y2)
                    pygame.draw.polygon(screen, RED, pts)


# ---------------------------------------------------------------------------
def update_status():
    """Update the contents of the status bar."""

    text = f'   Score {st.score}   '\
           f'Mirrors {st.mirrors}   '\
           f'Round {st.cycle}'
    text = INFO_FONT.render(text, True, WHITE)
    st_image.fill(GRAY)
    st_image.blit(text, (0, 5))


# ---------------------------------------------------------------------------
def new_game():
    """Display button to start a new game."""

    text = INFO_FONT.render('NEW GAME', True, WHITE)
    screen.blit(text, (400, (CELL_SIZE * 7) + 5))
    pygame.display.update()


# ---------------------------------------------------------------------------
def show_click():
    """Highlight the square that the player selected."""

    w = CELL_SIZE - 2
    x0 = (st.click_x * CELL_SIZE) + 1
    y0 = (st.click_y * CELL_SIZE) + 1
    pygame.draw.rect(screen, DARK_GRAY, (x0, y0, w, w))


# ---------------------------------------------------------------------------
def show_mirrors():
    """Paint the mirrors."""

    for y in range(7):
        for x in range(7):

            match st.grid[y][x]:
                case st.EMPTY:
                    continue
                case st.MIRROR2:
                    x0 = (x * CELL_SIZE) + 10
                    y0 = (y * CELL_SIZE) + 10
                    x1 = x0 + CELL_SIZE - 20
                    y1 = y0 + CELL_SIZE - 20
                    pygame.draw.line(screen, WHITE, (x0, y0), (x1, y1), width=7)
                case st.MIRROR1:
                    x0 = (x * CELL_SIZE) + CELL_SIZE - 10
                    y0 = (y * CELL_SIZE) + 10
                    x1 = x0 - CELL_SIZE + 20
                    y1 = y0 + CELL_SIZE - 20
                    pygame.draw.line(screen, WHITE, (x0, y0), (x1, y1), width=7)


# ---------------------------------------------------------------------------
def show_count(count):
    """Paint the countdown counter."""

    text = COUNT_FONT.render(count, True, YELLOW)
    rect = text.get_rect()
    rect.center = IMAGE_WIDTH // 2, IMAGE_HEIGHT // 2
    screen.blit(text, rect)
    pygame.display.update()


# ---------------------------------------------------------------------------
def get_xy(xy):
    """Convert from screen coordinates to grid coordinates."""

    return xy[0] // CELL_SIZE, xy[1] // CELL_SIZE


# ---------------------------------------------------------------------------
def show_intro():
    """Paint the intro text screen."""

    intro = (
        'The purpose of this game is to develop your short',
        'term memory. For each of 10 rounds, a set of diagonal',
        'mirrors will be briefly displayed. Then the mirrors',
        'are hidden and a laser cannon is displayed. You must',
        'determine at which point the laser beam will exit the',
        'grid, click on this gray square. If you are correct',
        'you get a point for each mirror on the grid, and the',
        'number of mirrors is increased. If you miss the number',
        'of mirrors is decreased. Good luck.',
        '',
        'Click here to start.',
    )

    st_image.fill(BG_COLOR)
    bg_image.fill(BG_COLOR)

    # Paint the game title
    text = HEADER_FONT.render('Laser Path', True, WHITE)
    rect = text.get_rect()
    rect.center = (IMAGE_WIDTH // 2, 40)
    bg_image.blit(text, rect)

    # Paint each line ot intro text
    y = 120
    for line in intro:
        text = INFO_FONT.render(line, True, WHITE)
        rect = text.get_rect()
        rect.center = (IMAGE_WIDTH // 2, y)
        bg_image.blit(text, rect)
        y += 40

    screen.blit(bg_image, (0, 0))
    screen.blit(st_image, (0, CELL_SIZE * 7))
    pygame.display.update()
    init_background()


# ---------------------------------------------------------------------------
def init_background():
    """Initialize the background image."""

    st_image.fill(GRAY)
    bg_image.fill(BLACK)
    w = CELL_SIZE - 2
    for y in range(7):
        for x in range(7):
            if x == 0 or x == 6 or y == 0 or y == 6:
                color = GRAY
            else:
                color = GREEN
            x0 = (x * CELL_SIZE) + 1
            y0 = (y * CELL_SIZE) + 1
            pygame.draw.rect(bg_image, color, (x0, y0, w, w))


# -----------------------------------------------------------------------
def fire_laser():
    """Animate the firing of a laser."""

    colors = (RED, YELLOW)
    color_flag = True

    for _ in range(30):
        color = RED if color_flag else YELLOW
        color_flag = not color_flag
        show_click()
        pygame.draw.lines(screen, color, False, laser_path, width=5)
        show_mirrors()
        show_laser()
        pygame.display.flip()
        sleep(0.1)

    laser_path.clear()


# ---------------------------------------------------------------------------
def laser_path_append(x, y):
    """Append a point to the laser beam path."""

    # Convert from grid coordinates to screen coordinates
    x0 = (x * CELL_SIZE) + HALF_CELL_SIZE
    y0 = (y * CELL_SIZE) + HALF_CELL_SIZE

    # If an edge cell, extend to edge of screen
    match [x, y]:
        case [0, _]: x0 = 0
        case [6, _]: x0 += HALF_CELL_SIZE
        case [_, 0]: y0 = 0
        case [_, 6]: y0 += HALF_CELL_SIZE

    laser_path.append((x0, y0))
