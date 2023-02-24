# ---------------------------------------------------------------------------
# Word Color
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame as pg
import state as st

IMAGE_WIDTH = 600
IMAGE_HEIGHT = 400

PAD = 20
BOX_HEIGHT = 100
BOX_WIDTH = (IMAGE_WIDTH - (3 * PAD)) // 2
BOX_TOP = (IMAGE_HEIGHT - BOX_HEIGHT) // 2
LEFT_BOX = PAD, BOX_TOP, BOX_WIDTH, BOX_HEIGHT
RIGHT_BOX = PAD + PAD + BOX_WIDTH, BOX_TOP, BOX_WIDTH, BOX_HEIGHT

LEFT_CENTER = IMAGE_WIDTH // 4, IMAGE_HEIGHT // 2
RIGHT_CENTER = 3 * IMAGE_WIDTH // 4, IMAGE_HEIGHT // 2


# Initialize pygame and setup the window
pg.init()
screen = pg.display.set_mode((IMAGE_WIDTH, IMAGE_HEIGHT))
pg.display.set_caption('Word Color   V1.1')

WORD_FONT = pg.font.SysFont('Arial', 80)
HEADER_FONT = pg.font.SysFont('Arial', 64)
INFO_FONT = pg.font.SysFont('Arial', 36)

BG_COLOR = 220, 220, 220
BLACK = 0, 0, 0
BLUE = 0, 0, 255
GREEN = 0, 160, 0
RED = 255, 0, 0
WHITE = 255, 255, 255
COLORS = (BLACK, BLUE, GREEN, RED)
WORDS = ('BLACK', 'BLUE', 'GREEN', 'RED')


# ---------------------------------------------------------------------------
def paint():
    """Paint the screen."""

    screen.fill(BG_COLOR)

    # Reminders
    text = f'WORD                           COLOR'
    text = INFO_FONT.render(text, True, BLACK)
    rect = text.get_rect()
    rect.center = IMAGE_WIDTH // 2, IMAGE_HEIGHT // 3
    screen.blit(text, rect)

    # Background boxes
    pg.draw.rect(screen, WHITE, LEFT_BOX)
    pg.draw.rect(screen, WHITE, RIGHT_BOX)

    # Paint the left side word
    word = WORDS[st.left_word]
    color = COLORS[st.left_color]
    text = HEADER_FONT.render(word, True, color)
    rect = text.get_rect()
    rect.center = LEFT_CENTER
    screen.blit(text, rect)

    # Paint the right side word
    word = WORDS[st.right_word]
    color = COLORS[st.right_color]
    text = HEADER_FONT.render(word, True, color)
    rect = text.get_rect()
    rect.center = RIGHT_CENTER
    screen.blit(text, rect)

    # When the round is over display the score
    if not st.game_active:
        text = f'Round {st.cycle}   Score {st.score} / {st.total}'
        text = INFO_FONT.render(text, True, BLACK)
        screen.blit(text, (10, IMAGE_HEIGHT - 50))

    pg.display.update()


# ---------------------------------------------------------------------------
def paint_intro():
    """Paint the intro text screen."""

    intro = (
        'In this game you must determine if the',
        'meaning of the word on the left matches the',
        'color of the word on the right.',
        'If they match, press the right arrow key.',
        'If they do not match, press the left arrow key.',
        'You have 30 seconds for each round.',
        'Press the space bar to start a round.',
    )

    screen.fill(BG_COLOR)

    # Paint the game title
    text = HEADER_FONT.render('Word Color', True, BLACK)
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
        y += 45

    pg.display.update()
