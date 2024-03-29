# ---------------------------------------------------------------------------
# Origami
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame as pg
import state as st

CELL_SIZE = 60
IMAGE_WIDTH = 9 * CELL_SIZE
IMAGE_HEIGHT = 10 * CELL_SIZE
STATUS_LOC = (0, (9 * CELL_SIZE) + 10)

# Initialize pygame and setup the window
pg.init()
screen = pg.display.set_mode((IMAGE_WIDTH, IMAGE_HEIGHT))
pg.display.set_caption('Origami   V1.4')

BG_SIZE = 8 * CELL_SIZE
bg_image = pg.Surface((BG_SIZE, BG_SIZE))
offset_x = 0
offset_y = 0

HEADER_FONT = pg.font.SysFont('Arial', 64)
INFO_FONT = pg.font.SysFont('Arial', 32)

WHITE = 255, 255, 255
BLACK = 0, 0, 0
GREEN = 0, 127, 0
GRAY = 127, 127, 127
DARK_GRAY = 96, 96, 96
YELLOW = 255, 255, 0
RED = 255, 0, 0

IM_X = pg.image.load(r'Images\X.png')
IM_C = pg.image.load(r'Images\Clubs.png')
IM_D = pg.image.load(r'Images\Diamond.png')
IM_H = pg.image.load(r'Images\Heart.png')
IM_S = pg.image.load(r'Images\Spades.png')
IMAGES = None, IM_C, IM_D, IM_H, IM_S, IM_X


# ---------------------------------------------------------------------------
def paint():
    """Paint the screen."""

    screen.fill(WHITE)
    screen.blit(bg_image, (CELL_SIZE // 2, CELL_SIZE // 2))

    # If the mouse pointer is over a blank cell,
    # fill that cell with an card image
    if st.cursor_x >= 0:
        cell = st.grid[st.cursor_y][st.cursor_x]
        if cell == st.IMG_BLANK:
            img = IMAGES[st.cursor_img]
            x = (st.cursor_x * CELL_SIZE) + offset_x + 14
            y = (st.cursor_y * CELL_SIZE) + offset_y + 14
            screen.blit(img, (x, y))

    # Paint the status bar
    if st.state == st.ST_IDLE:
        text = f' Score {st.score}/10  Time {st.start_time:.1f} Seconds'
        text = INFO_FONT.render(text, True, BLACK)
        screen.blit(text, STATUS_LOC)

    pg.display.update()


# ---------------------------------------------------------------------------
def paint_pattern():
    """Paint the outline of the paper showing the folds."""

    global offset_x, offset_y

    # There is a separate routine for each type of fold
    match st.flip:
        case st.FLIP_NONE: paint_none()
        case st.FLIP_HORZ: paint_horz()
        case st.FLIP_VERT: paint_vert()
        case st.FLIP_BOTH: paint_both()
        case st.FLIP_DIAG: paint_diag()

    # Add the card images
    for y, line in enumerate(st.grid):
        for x, cell in enumerate(line):
            if cell > st.IMG_BLANK:
                img = IMAGES[cell]
                x0 = offset_x + (x * CELL_SIZE) + 14
                y0 = offset_y + (y * CELL_SIZE) + 14
                bg_image.blit(img, (x0, y0))

    # Adjust offsets to account for border
    offset_x += CELL_SIZE // 2
    offset_y += CELL_SIZE // 2


# ---------------------------------------------------------------------------
def paint_none():
    """Paint a paper with no flips."""

    global offset_x, offset_y

    # Clear the prevoius image
    bg_image.fill(WHITE)

    # Set offsets from upper left corner of image to the
    # upper left cornet of the paper
    offset_x = (BG_SIZE - (st.paper_w * CELL_SIZE)) // 2
    offset_y = (BG_SIZE - (st.paper_h * CELL_SIZE)) // 2

    # Draw the border of the paper
    p0 = offset_x, offset_y
    wh = st.paper_w * CELL_SIZE, st.paper_h * CELL_SIZE
    pg.draw.rect(bg_image, BLACK, (p0, wh), width=3)


# ---------------------------------------------------------------------------
def paint_horz():
    """Paint a paper with a horizontal fold."""

    global offset_x, offset_y

    # Clear the prevoius image
    bg_image.fill(WHITE)

    # Set offsets from upper left corner of image to the
    # upper left cornet of the paper
    offset_x = (BG_SIZE - (st.paper_w * 2 * CELL_SIZE)) // 2
    offset_y = (BG_SIZE - (st.paper_h * CELL_SIZE)) // 2

    # Draw the border of the paper
    p0 = offset_x, offset_y
    wh = st.paper_w * 2 * CELL_SIZE, st.paper_h * CELL_SIZE
    pg.draw.rect(bg_image, BLACK, (p0, wh), width=3)

    # Draw a line for the fold
    x0 = offset_x + (st.paper_w * CELL_SIZE)
    y0 = offset_y
    x1 = offset_x + (st.paper_w * CELL_SIZE)
    y1 = offset_y + (st.paper_h * CELL_SIZE)
    pg.draw.line(bg_image, BLACK, (x0, y0), (x1, y1))


# ---------------------------------------------------------------------------
def paint_vert():
    """Paint a paper with a vertical fold."""

    global offset_x, offset_y

    # Clear the prevoius image
    bg_image.fill(WHITE)

    # Set offsets from upper left corner of image to the
    # upper left cornet of the paper
    offset_x = (BG_SIZE - (st.paper_w * CELL_SIZE)) // 2
    offset_y = (BG_SIZE - (st.paper_h * 2 * CELL_SIZE)) // 2

    # Draw the border of the paper
    p0 = offset_x, offset_y
    wh = st.paper_w * CELL_SIZE, st.paper_h * 2 * CELL_SIZE
    pg.draw.rect(bg_image, BLACK, (p0, wh), width=3)

    # Draw a line for the fold
    x0 = offset_x
    y0 = offset_y + (st.paper_h * CELL_SIZE)
    x1 = offset_x + (st.paper_w * CELL_SIZE)
    y1 = offset_y + (st.paper_h * CELL_SIZE)
    pg.draw.line(bg_image, BLACK, (x0, y0), (x1, y1))


# ---------------------------------------------------------------------------
def paint_both():
    """Paint a paper with both a horizontal and a vertical fold."""

    global offset_x, offset_y

    # Clear the prevoius image
    bg_image.fill(WHITE)

    # Set offsets from upper left corner of image to the
    # upper left cornet of the paper
    offset_x = (BG_SIZE - (st.paper_w * 2 * CELL_SIZE)) // 2
    offset_y = (BG_SIZE - (st.paper_h * 2 * CELL_SIZE)) // 2

    # Draw the border of the paper
    p0 = offset_x, offset_y
    wh = st.paper_w * 2 * CELL_SIZE, st.paper_h * 2 * CELL_SIZE
    pg.draw.rect(bg_image, BLACK, (p0, wh), width=3)

    # Draw lines for the folds
    x0 = offset_x
    y0 = offset_y + (st.paper_h * CELL_SIZE)
    x1 = offset_x + (st.paper_w * 2 * CELL_SIZE)
    y1 = offset_y + (st.paper_h * CELL_SIZE)
    pg.draw.line(bg_image, BLACK, (x0, y0), (x1, y1))
    x0 = offset_x + (st.paper_w * CELL_SIZE)
    y0 = offset_y
    x1 = offset_x + (st.paper_w * CELL_SIZE)
    y1 = offset_y + (st.paper_h * 2 * CELL_SIZE)
    pg.draw.line(bg_image, BLACK, (x0, y0), (x1, y1))


# ---------------------------------------------------------------------------
def paint_diag():
    """Paint a paper with a diagonal fold."""

    global offset_x, offset_y

    # Clear the prevoius image
    bg_image.fill(WHITE)

    # Set offsets from upper left corner of image to the
    # upper left cornet of the paper
    w = st.paper_w + 1
    h = st.paper_h + 1
    offset_x = (BG_SIZE - (w * CELL_SIZE)) // 2
    offset_y = (BG_SIZE - (h * CELL_SIZE)) // 2

    # Draw the border of the paper
    p0 = offset_x, offset_y
    wh = w * CELL_SIZE, h * CELL_SIZE
    pg.draw.rect(bg_image, BLACK, (p0, wh), width=3)

    # Draw a line for the fold
    x0 = offset_x
    y0 = offset_y
    x1 = offset_x + (w * CELL_SIZE)
    y1 = offset_y + (h * CELL_SIZE)
    pg.draw.line(bg_image, BLACK, (x0, y0), (x1, y1))


# ---------------------------------------------------------------------------
def get_xy(xy):
    """Convert from screen coordinates to grid coordinates."""

    # Get the grid coordinates
    x = (xy[0] - offset_x) // CELL_SIZE
    y = (xy[1] - offset_y) // CELL_SIZE

    # Determine max values depending on the folds
    max_x = st.paper_w
    max_y = st.paper_h
    match st.flip:
        case st.FLIP_HORZ:
            max_x *= 2
        case st.FLIP_VERT:
            max_y *= 2
        case st.FLIP_BOTH:
            max_x *= 2
            max_y *= 2
        case st.FLIP_DIAG:
            if x == y:
                return -1, -1
            max_x += 1
            max_y += 1

    # Determine if coordinates are on the paper
    if 0 <= x < max_x and 0 <= y < max_y:
        return x, y
    else:
        return -1, -1


# ---------------------------------------------------------------------------
def show_intro():
    """Paint the intro text screen."""

    intro = (
        "This game is about placing symbols",
        "on a piece of very thin paper, then",
        "folding the paper so that all the",
        "symbols can be seen. Your job is to",
        "place the last symbol where it will",
        "not overlap any other symbols when",
        "the paper is folded.",
        "",
        'Click to start a game.',
    )

    # Paint the game title
    screen.fill(WHITE)
    text = HEADER_FONT.render('Origami', True, BLACK)
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
        y += 50

    pg.display.update()
