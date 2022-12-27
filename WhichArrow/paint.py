# ---------------------------------------------------------------------------
# Which Arrow
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame
import state as st

from random import randrange

IMAGE_WIDTH = 600
IMAGE_HEIGHT = 600

# Initialize pygame and setup the window
pygame.init()
screen = pygame.display.set_mode((IMAGE_WIDTH, IMAGE_HEIGHT))
pygame.display.set_caption('Which Arrow   V1.0')

HEADER_FONT = pygame.font.SysFont('Arial', 48)
INFO_FONT = pygame.font.SysFont('Arial', 36)

BG_COLOR = 245, 222, 179
BLACK = 0, 0, 0

ARROW_RT = pygame.image.load('Images/arrow_rt.png')
ARROW_LF = pygame.image.load('Images/arrow_lf.png')
ARROW_UP = pygame.image.load('Images/arrow_up.png')
ARROW_DN = pygame.image.load('Images/arrow_dn.png')
ARROWS = (ARROW_UP, ARROW_RT, ARROW_DN, ARROW_LF)

PATTERN0 = ((0, 0), (0, 25), (0, 50), (0, 75), (0, 100))
PATTERN1 = ((100, 0), (75, 25), (50, 50), (25, 75), (0, 100))
PATTERN2 = ((0, 0), (25, 0), (50, 0), (75, 0), (100, 0))
PATTERN3 = ((0, 0), (25, 25), (50, 50), (75, 75), (100, 100))
PATTERN4 = ((0, 50), (25, 25), (50, 0), (75, 25), (100, 50))
PATTERN5 = ((0, 0), (25, 25), (50, 50), (25, 75), (0, 100))
PATTERN6 = ((0, 0), (25, 25), (50, 50), (75, 25), (100, 0))
PATTERN7 = ((100, 0), (75, 25), (50, 50), (75, 75), (100, 100))
PATTERNS = (PATTERN0, PATTERN1, PATTERN2, PATTERN3,
            PATTERN4, PATTERN5, PATTERN6, PATTERN7)


# ---------------------------------------------------------------------------
def paint():
    """Paint the screen."""

    screen.fill(BG_COLOR)
    if st.game_active:
        paint_arrows()
    else:
        paint_score()
    pygame.display.update()


# ---------------------------------------------------------------------------
def paint_arrows():
    """Paint a random pattern of arrows."""

    side_img = ARROWS[randrange(4)]
    st.main_arrow = randrange(4)
    main_img = ARROWS[st.main_arrow]
    pattern = PATTERNS[randrange(8)]
    offset_x = randrange(10, 450)
    offset_y = randrange(10, 450)

    for i, xy in enumerate(pattern):
        x, y = xy
        img = side_img if i != 2 else main_img
        screen.blit(img, (offset_x + x, offset_y + y))


# ---------------------------------------------------------------------------
def paint_score():
    """Paint the score and message to start new game."""

    text = f'Score {st.score}   Total {st.total}'
    text = HEADER_FONT.render(text, True, BLACK)
    rect = text.get_rect()
    rect.center = 300, 250
    screen.blit(text, rect)

    text = f'Press space bar to start again'
    text = INFO_FONT.render(text, True, BLACK)
    rect = text.get_rect()
    rect.center = 300, 300
    screen.blit(text, rect)


# ---------------------------------------------------------------------------
def paint_intro():
    """Paint the intro text screen."""

    intro = (
        'The purpose of this game is to',
        'determine the direction of the arrow',
        'at the center of the 5 arrow pattern.',
        'Use the 4 arrow keys indicate the',
        'correct direction.',
        'You have 45 seconds.',
        'Press the space bar to start a game.',
        'Good luck.',
    )

    screen.fill(BG_COLOR)

    # Paint the game title
    text = HEADER_FONT.render('Which Arrow', True, BLACK)
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

    pygame.display.update()
