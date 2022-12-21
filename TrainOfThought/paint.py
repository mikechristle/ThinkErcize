# ---------------------------------------------------------------------------
# ThinkErcise
# Paint the screen
# Mike Christle 2022
# ---------------------------------------------------------------------------

import state as st
import pygame
import images

from enum_types import DirT, FuncT

CELL_SIZE = 36

IMAGE_WIDTH = st.GRID_WIDTH * CELL_SIZE
IMAGE_HEIGHT = st.GRID_HEIGHT * CELL_SIZE

# Initialize pygame and setup the window
pygame.init()
screen = pygame.display.set_mode((IMAGE_WIDTH, IMAGE_HEIGHT + CELL_SIZE))
pygame.display.set_caption('Train Of Thought   V0.1')

bg_image = pygame.Surface((IMAGE_WIDTH, IMAGE_HEIGHT))
btn_image = pygame.Surface((IMAGE_WIDTH, CELL_SIZE))

BUTTON_FONT = pygame.font.SysFont('Arial', 36)
HEADER_FONT = pygame.font.SysFont('Arial', 72)
INFO_FONT = pygame.font.SysFont('Arial', 48)

BG_COLOR = 107, 142, 35
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# ---------------------------------------------------------------------------
def get_xy(xy):
    """Convert from screen coordinates to grid coordinates."""

    return xy[0] // CELL_SIZE, xy[1] // CELL_SIZE


# ---------------------------------------------------------------------------
def paint():
    """Paint the screen."""

    # Clear the previous screen
    screen.fill(BG_COLOR)

    # Paint the tracks, turns, tunnel and barns
    screen.blit(bg_image, (0, 0))

    # If game is done, paint the button bar
    if not st.game_active:
        screen.blit(btn_image, (0, IMAGE_HEIGHT))

    # Paint switches
    for x, y, dir_f, dir_t, flag in st.switches:
        match [dir_f, dir_t, flag]:
            case [DirT.RIGHT | DirT.LEFT, _, False]:
                img = images.SWITCH_H
            case [DirT.UP | DirT.DOWN, _, False]:
                img = images.SWITCH_V
            case [DirT.RIGHT, DirT.UP, True]:
                img = images.SWITCH_UL
            case [DirT.RIGHT, DirT.DOWN, True]:
                img = images.SWITCH_DR
            case [DirT.LEFT, DirT.UP, True]:
                img = images.SWITCH_UR
            case [DirT.LEFT, DirT.DOWN, True]:
                img = images.SWITCH_DL
            case [DirT.UP, DirT.LEFT, True]:
                img = images.SWITCH_DR
            case [DirT.UP, DirT.RIGHT, True]:
                img = images.SWITCH_DL
            case [DirT.DOWN, DirT.LEFT, True]:
                img = images.SWITCH_UL
            case [DirT.DOWN, DirT.RIGHT, True]:
                img = images.SWITCH_UR

        screen.blit(img, (x * CELL_SIZE, y * CELL_SIZE))

    # Paint Trains
    for x, y, color in st.trains:
        match st.grid[y][x]:
            case [FuncT.SWITCH, idx]:
                _, _, d0, d1, flag = st.switches[idx]
                direction = d1 if flag else d0
                img = images.TRAIN_IMGS[color][direction.value]
            case [FuncT.TURN | FuncT.BARN, direction, _]:
                img = images.TRAIN_IMGS[color][direction.value]
            case [_, direction]:
                img = images.TRAIN_IMGS[color][direction.value]
        screen.blit(img, (x * CELL_SIZE, y * CELL_SIZE))

    pygame.display.flip()


# ---------------------------------------------------------------------------
def paint_intro():
    """Paint the intro text screen."""

    intro = (
        'Your job is to route each train',
        'to the barn with the same color.',
        'Select a level of difficulty from',
        '4 to 8, then press START.',
        'Click on the blue circles to',
        'toggle the switches.',
        'Good luck.',
    )

    bg_image.fill(BG_COLOR)

    # Paint the game title
    text = HEADER_FONT.render('Train of Thought', True, WHITE)
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
        y += 60

    pygame.display.update()


# ---------------------------------------------------------------------------
def paint_btns():
    """Paint the button bar."""

    btn_image.fill(BG_COLOR)

    # Paint difficulty levels
    for idx in range(4, 9):
        color = BLACK if idx != st.difficulty_level else WHITE
        text = BUTTON_FONT.render(str(idx), True, color)
        rect = text.get_rect()
        rect.top = 0
        rect.left = (idx - 3) * CELL_SIZE
        btn_image.blit(text, rect)

    # Paint start button
    text = BUTTON_FONT.render('START', True, WHITE)
    rect = text.get_rect()
    rect.top = 0
    rect.left = (st.GRID_WIDTH - 3) * CELL_SIZE
    btn_image.blit(text, rect)

    # Paint score
    if st.total_trains > 0:
        text = f'{st.game_score}/{st.total_trains}'
        text = BUTTON_FONT.render(text, True, WHITE)
        rect = text.get_rect()
        rect.top = 0
        rect.left = 10 * CELL_SIZE
        btn_image.blit(text, rect)


# ---------------------------------------------------------------------------
def init_tracks():
    """
    Initialize the background image with tunnel, tracks and barns.
    These elements do not change during the game, so they only need
    to be painted once.
    """

    bg_image.fill(BG_COLOR)

    # For each grid cell
    for y in range(st.GRID_HEIGHT):
        for x in range(st.GRID_WIDTH):
            cell = st.grid[y][x]

            # Get an image for each cell
            match cell:
                case [FuncT.TUNNEL, DirT.UP]:
                    img = images.TUNNEL_U
                case [FuncT.TUNNEL, DirT.DOWN]:
                    img = images.TUNNEL_D
                case [FuncT.TUNNEL, DirT.RIGHT]:
                    img = images.TUNNEL_R
                case [FuncT.TUNNEL, DirT.LEFT]:
                    img = images.TUNNEL_L
                case [FuncT.BARN, dir, color]:
                    img = images.BARN_IMGS[color][dir.value]
                case [FuncT.TRACK, DirT.DOWN | DirT.UP]:
                    img = images.TRACK_V
                case [FuncT.TRACK, DirT.RIGHT | DirT.LEFT]:
                    img = images.TRACK_H
                case [FuncT.TURN, _, idx]:
                    img = images.TURN_IMGS[idx.value]
                case _:
                    continue

            # Paint the image
            bg_image.blit(img, (x * CELL_SIZE, y * CELL_SIZE))
