# ---------------------------------------------------------------------------
# Origami
# Mike Christle 2022
# ---------------------------------------------------------------------------

import sys
import pygame
import state

from paint import paint, get_xy, show_intro
from logic import set_pattern, check_click

# 0.25 Second timer event
pygame.time.set_timer(pygame.USEREVENT, 250)

show_intro()
delay_count = 0

while True:

    # Get all pygame events
    for event in pygame.event.get():
        match event.type:

            # Exit if window is closed
            case pygame.QUIT:
                sys.exit()

            # Any click starts the game
            case pygame.MOUSEBUTTONDOWN if state.state == state.ST_IDLE:
                state.state = state.ST_WAIT
                set_pattern()
                paint()

            # Move the cursor over the image
            case pygame.MOUSEMOTION if state.state == state.ST_WAIT:
                x, y = get_xy(event.pos)
                if x >= 0:
                    state.cursor_x = x
                    state.cursor_y = y
                    paint()

            # Player selects a position
            case pygame.MOUSEBUTTONDOWN if state.state == state.ST_WAIT:
                if check_click():
                    paint()
                    delay_count = 10
                    state.state = state.ST_DONE

            # Delay 5 seconds then start a new game
            case pygame.USEREVENT if state.state == state.ST_DONE:
                delay_count -= 1
                if delay_count == 0:
                    state.state = state.ST_WAIT
                    set_pattern()
                    paint()
