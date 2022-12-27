# ---------------------------------------------------------------------------
# Best Route
# Mike Christle 2022
# ---------------------------------------------------------------------------


import pygame
import state as st

from images import DOGS, HOUSES, CAR

CELL_SIZE = 60
HALF_CELL = CELL_SIZE // 2
IMAGE_WIDTH = 9 * CELL_SIZE
IMAGE_HEIGHT = (10 * CELL_SIZE) + HALF_CELL

LINE_WIDTH = CELL_SIZE - 11
CIRCLE_RADIUS = LINE_WIDTH // 2

CAR_X0 = IMAGE_WIDTH - (3 * CELL_SIZE)
CAR_X1 = CAR_X0 + CELL_SIZE
CAR_X2 = CAR_X0 + CELL_SIZE + CELL_SIZE
CAR_Y0 = IMAGE_HEIGHT - CELL_SIZE - HALF_CELL
CAR_P0 = CAR_X0, CAR_Y0
CAR_P1 = CAR_X1, CAR_Y0
CAR_P2 = CAR_X2, CAR_Y0

LEVEL_SPACE = 48
LEVEL_X0 = CELL_SIZE
LEVEL_Y0 = IMAGE_HEIGHT - LEVEL_SPACE
LEVEL_Y1 = LEVEL_Y0 - LEVEL_SPACE
START_X0 = 3 * IMAGE_WIDTH // 4

# Initialize pygame and setup the window
pygame.init()
screen = pygame.display.set_mode((IMAGE_WIDTH, IMAGE_HEIGHT))
pygame.display.set_caption('Best Route   V1.0')

bg_image = pygame.Surface((IMAGE_WIDTH, IMAGE_HEIGHT))
offset = 0

HEADER_FONT = pygame.font.SysFont('Arial', 52)
TEXT_FONT = pygame.font.SysFont('Arial', 30)
LEVEL_FONT = pygame.font.SysFont('Arial', 40)
STATUS_FONT = pygame.font.SysFont('Arial', 30)

BG_COLOR = 62, 142, 0
WHITE = 255, 255, 255
YELLOW = 255, 255, 0
BLACK = 0, 0, 0
BLUE = 0, 0, 255
GRAY = 64, 64, 64
GREEN = 0, 255, 0
RED = 255, 0, 0
COLORS = (None, GREEN, GREEN, RED)


# ---------------------------------------------------------------------------
def paint():
    """Paint the screen."""

    screen.blit(bg_image, (0, 0))
    paint_maze()
    paint_car()
    pygame.display.update()


# ---------------------------------------------------------------------------
def paint_maze():
    """Paint the car, dogs and houses on the maze."""

    for y in range(st.level):
        y0 = (y * CELL_SIZE) + offset + HALF_CELL
        for x in range(st.level):
            x0 = (x * CELL_SIZE) + offset + HALF_CELL
            val = st.maze[y][x].val
            if val >= 20:
                img = DOGS[val - 20]
            elif val >= 10:
                img = HOUSES[val - 10]
            elif val == 1:
                img = CAR
            else:
                continue

            rect = img.get_rect()
            rect.center = x0, y0
            screen.blit(img, rect)


# ---------------------------------------------------------------------------
def paint_car():
    """Paint the dogs that are in the car, and the miles traveled."""

    # Paint dogs in the car
    x0 = CAR_X0
    for dog in st.car:
        img = DOGS[dog - 20]
        rect = img.get_rect()
        rect.center = x0, CAR_Y0
        screen.blit(img, rect)
        x0 += CELL_SIZE

    # Paint miles traveled
    if st.miles > 0:
        text = f'{st.miles} Miles'
        text = LEVEL_FONT.render(text, True, WHITE)
        screen.blit(text, (LEVEL_X0, LEVEL_Y1))


# ---------------------------------------------------------------------------
def build_background():
    """Paint the maze on the background image."""

    # Offset is the distance in pixels to the first cell
    global offset
    offset = (IMAGE_WIDTH - (st.level * CELL_SIZE)) // 2

    bg_image.fill(BG_COLOR)

    # For eac cell in the maze
    for y in range(st.level):
        y0 = (y * CELL_SIZE) + offset + HALF_CELL
        for x in range(st.level):
            x0 = (x * CELL_SIZE) + offset + HALF_CELL
            cell = st.maze[y][x]

            # If no wall on right side, paint a road
            if cell.rit:
                x1 = x0 + CELL_SIZE
                pygame.draw.line(bg_image, GRAY,
                                 (x0, y0), (x1, y0), width=LINE_WIDTH)

            # If no wall below, paint a road
            if cell.bot:
                y1 = y0 + CELL_SIZE
                pygame.draw.line(bg_image, GRAY,
                                 (x0, y0), (x0, y1), width=LINE_WIDTH)

            # Paint a circle and a yellow dot on each cell
            pygame.draw.circle(bg_image, GRAY, (x0, y0), CIRCLE_RADIUS)
            pygame.draw.circle(bg_image, YELLOW, (x0, y0), 3)

    # Draw the background for the car
    pygame.draw.line(bg_image, GRAY, CAR_P0, CAR_P2, width=LINE_WIDTH)
    pygame.draw.circle(bg_image, GRAY, CAR_P0, CIRCLE_RADIUS)
    pygame.draw.circle(bg_image, GRAY, CAR_P2, CIRCLE_RADIUS)


# ---------------------------------------------------------------------------
def paint_status():
    """Paint the level and start button."""

    # Paint levels
    x0 = LEVEL_X0
    for level in range(4, 9):
        color = WHITE if level == st.level else BLACK
        text = LEVEL_FONT.render(str(level), True, color)
        screen.blit(text, (x0, LEVEL_Y0))
        x0 += LEVEL_SPACE

    # Paint start button
    text = LEVEL_FONT.render('START', True, WHITE)
    screen.blit(text, (START_X0, LEVEL_Y0))

    pygame.display.update()


# ---------------------------------------------------------------------------
def get_level(xy):
    """
    Decode screen coordinates to return level or start command.
    Returns 0 if nothing clicked.
    Returns 4-8 for a level.
    Returns 10 for start command.
    """

    if xy[1] < LEVEL_Y0:
        return 0

    if xy[0] > START_X0:
        return 10

    if xy[0] < LEVEL_X0 or xy[0] > (LEVEL_X0 + (5 * LEVEL_SPACE)):
        return 0

    return ((xy[0] - LEVEL_X0) // LEVEL_SPACE) + 4


# ---------------------------------------------------------------------------
def get_xy(xy):
    """Decode screen coordinates to return cell coordinates."""

    return (xy[0] - offset) // CELL_SIZE, (xy[1] - offset) // CELL_SIZE


# ---------------------------------------------------------------------------
def show_intro():
    """Paint the intro text screen."""

    intro = (
        'Your job is to find stray dogs and return them',
        'to their homes. You have a small car, so you',
        'can only carry up to three dogs at a time.',
        'Since you don\'t have all day, you must find',
        'the shortest route possible.',
        '',
        'Your position is marked by the car. To make it',
        'move, click on a dog or a house and it will',
        'drive to that position by the shortest path.',
        '',
        'Click to start game.',
    )

    # Paint the game title
    screen.fill(BG_COLOR)
    text = HEADER_FONT.render('Digit Order', True, WHITE)
    rect = text.get_rect()
    rect.center = (IMAGE_WIDTH // 2, 30)
    screen.blit(text, rect)

    # Paint each line ot intro text
    y = 120
    for line in intro:
        text = TEXT_FONT.render(line, True, WHITE)
        rect = text.get_rect()
        rect.center = (IMAGE_WIDTH // 2, y)
        screen.blit(text, rect)
        y += 35

    pygame.display.update()
