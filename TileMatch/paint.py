# ---------------------------------------------------------------------------
# Tile Match
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame
import state as st

CELL_SIZE = 50
HALF_CELL_SIZE = CELL_SIZE // 2
IMAGE_WIDTH = 100 + (10 * CELL_SIZE) + 20
IMAGE_HEIGHT = 20 + (10 * CELL_SIZE) + 100
FIELD_RECT = 100, 20, 10 * CELL_SIZE, 10 * CELL_SIZE
NEW_TILE_LOC = 50, IMAGE_HEIGHT // 2

OFFSET_X = 100 + (3 * CELL_SIZE // 2)
OFFSET_Y = 20 + (3 * CELL_SIZE // 2)

# Initialize pygame and setup the window
pygame.init()
screen = pygame.display.set_mode((IMAGE_WIDTH, IMAGE_HEIGHT))
pygame.display.set_caption('Tile Match   V1.1')

BG_SIZE = 8 * CELL_SIZE
bg_image = pygame.Surface((BG_SIZE, BG_SIZE))
offset_x = 0
offset_y = 0

HEADER_FONT = pygame.font.SysFont('Arial', 60)
INFO_FONT = pygame.font.SysFont('Arial', 28)

WHITE = 255, 255, 255
BLACK = 0, 0, 0
GREEN = 0, 192, 0
GRAY = 192, 192, 192
YELLOW = 255, 255, 0
RED = 255, 0, 0
COLORS = RED, YELLOW, GREEN

STAT0_LOC = 200, 520
STAT1_LOC = 200, 560

HELP_MSG = INFO_FONT.render('Tall = Color    Wide = Shape', True, BLACK)
STAT1_MSG = INFO_FONT.render('Click to start a new round', True, BLACK)

IM_CIRCLE = pygame.image.load(r'Images\Circle.png')
IM_DIAMOND = pygame.image.load(r'Images\Diamond.png')
IM_SQUARE = pygame.image.load(r'Images\Squares.png')
IMAGES = None, None, IM_SQUARE, IM_DIAMOND, IM_CIRCLE

VERT_RECT = pygame.Rect(0, 0, CELL_SIZE - 14, CELL_SIZE + 14)
HORZ_RECT = pygame.Rect(0, 0, CELL_SIZE + 14, CELL_SIZE - 14)
RECTS = VERT_RECT, HORZ_RECT

TIMER_LOC = 80 + (5 * CELL_SIZE), 4 * CELL_SIZE


# ---------------------------------------------------------------------------
def paint():
    """Paint the screen."""

    screen.fill(GRAY)
    pygame.draw.rect(screen, BLACK, FIELD_RECT)

    if st.state == st.ST_PLAY:
        paint_tiles()
        paint_tile(st.new_tile)
        screen.blit(HELP_MSG, STAT0_LOC)
    elif st.state == st.ST_START:
        msg = f'{st.delay_count}'
        msg = HEADER_FONT.render(msg, True, YELLOW)
        screen.blit(msg, TIMER_LOC)
    else: # st.state == st.ST_IDLE
        msg = f'Run Time {st.run_time} seconds'
        msg = INFO_FONT.render(msg, True, BLACK)
        screen.blit(msg, STAT0_LOC)
        screen.blit(STAT1_MSG, STAT1_LOC)

    pygame.display.update()


# ---------------------------------------------------------------------------
def paint_tiles():
    """Paint the tiles from the grid."""

    for y in range(8):
        for x in range(8):
            tile = st.grid[y][x]
            if tile.shape != st.BLANK:
                paint_tile(tile)


# ---------------------------------------------------------------------------
def paint_tile(tile):
    """Paint a single tile."""

    rect = RECTS[tile.orient]
    rect.center = tile.x0, tile.y0
    if tile.shape != st.BORDER:
        color = COLORS[tile.color]
        pygame.draw.rect(screen, color, rect)
    shape = IMAGES[tile.shape]
    if shape != None:
        screen.blit(shape,  (rect.center[0] - 10, rect.center[1] - 10))
    pygame.draw.rect(screen, WHITE, rect, width=1)


# ---------------------------------------------------------------------------
def get_xy(xy):
    """Convert from screen coordinates to grid coordinates."""

    x = (xy[0] - OFFSET_X + HALF_CELL_SIZE) // CELL_SIZE
    y = (xy[1] - OFFSET_Y + HALF_CELL_SIZE) // CELL_SIZE
    return x, y


# ---------------------------------------------------------------------------
def init_tiles():
    """
    Initialize the x and y screen coordinates of
    each cell in the grid, and the new tile.
    """

    for y in range(8):
        for x in range(8):
            st.grid[y][x].x0 = (x * CELL_SIZE) + OFFSET_X
            st.grid[y][x].y0 = (y * CELL_SIZE) + OFFSET_Y

    st.new_tile.x0 = 50
    st.new_tile.y0 = IMAGE_HEIGHT // 2


# ---------------------------------------------------------------------------
def show_intro():
    """Paint the intro text screen."""

    intro = (
        'The object of this game is to eliminate all of the tiles',
        'as fast as possible. Tiles have one of three colors,',
        'and one of three shaped inlays.',
        'As each new tile is displayed on the left side,',
        'you must place it on the grid next to matching tiles.',
        'If the new tile is tall then the colors must match.',
        'If the new tile is wide then the inlays must match.',
        'Matching tiles are then removed from the grid.',
        '',
        'Click here to start.',
    )

    # Paint the game title
    screen.fill(GRAY)
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

    pygame.display.update()
