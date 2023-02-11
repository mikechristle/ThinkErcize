# ---------------------------------------------------------------------------
# MathTest
# Mike Christle 2023
# ---------------------------------------------------------------------------

import pygame as py
import state as st

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480

# Initialize pygame and setup the window
py.init()
screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
py.display.set_caption("MathTest   V1.0")

HEADER_FONT = py.font.SysFont('Arial', 64)
INFO_FONT = py.font.SysFont('Arial', 32)
TEXT_FONT = py.font.SysFont('Arial', 64)

WHITE = 255, 255, 255
BLACK = 0, 0, 0
GREEN = 0, 250, 0

LEFT_RECT = 40, 240, 320, 74
RIGHT_RECT = 440, 240, 320, 74
LEFT_CENTER = 200, 270
RIGHT_CENTER = 600, 270

INSTRUCTIONS = (
    'Right arrow if right expression is greater.',
    'Left arrow if left expression is greater.',
    'Up or down arrow if expressions are equal.'
)


# ---------------------------------------------------------------------------
def paint():
    """Paint the screen."""

    screen.fill(GREEN)

    py.draw.rect(screen, WHITE, LEFT_RECT)
    py.draw.rect(screen, WHITE, RIGHT_RECT)

    # Paint each line ot intro text
    y = 60
    for line in INSTRUCTIONS:
        center_text(line, y)
        y += 45

    # Paint the left expression
    text = TEXT_FONT.render(st.eq_left, True, BLACK)
    rect = text.get_rect()
    rect.center = LEFT_CENTER
    screen.blit(text, rect)

    # Paint the right expression
    text = TEXT_FONT.render(st.eq_right, True, BLACK)
    rect = text.get_rect()
    rect.center = RIGHT_CENTER
    screen.blit(text, rect)

    # If game over, paint the results
    if not st.game_active:
        text = f'Score {st.score}/20       Time {st.time:.1f} Seconds.'
        center_text(text, 380)
        text = 'Press space to start next round.'
        center_text(text, 430)

    py.display.update()


# ---------------------------------------------------------------------------
def paint_intro():
    """Paint the intro text screen."""

    intro = (
        "You will be shown two simple math expressions.",
        "You must solve each and decide which has the greater value.",
        "If the right is greater, press the right arrow key.",
        "If the left is greater, press the left arrow key.",
        "I they are the same, press the up or down arrow keys.",
        "",
        "Press space bar to start."
    )

    screen.fill(GREEN)

    # Paint the game title
    text = HEADER_FONT.render("MathTest", True, BLACK)
    rect = text.get_rect()
    rect.center = (SCREEN_WIDTH // 2, 40)
    screen.blit(text, rect)

    # Paint each line ot intro text
    y = 150
    for line in intro:
        center_text(line, y)
        y += 45

    py.display.update()


# ---------------------------------------------------------------------------
def center_text(text, pos_y):
    """Paint a line of text centered on the screen."""

    text = INFO_FONT.render(text, True, BLACK)
    rect = text.get_rect()
    rect.center = (SCREEN_WIDTH // 2, pos_y)
    screen.blit(text, rect)
