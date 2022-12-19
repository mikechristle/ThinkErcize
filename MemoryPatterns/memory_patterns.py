# ---------------------------------------------------------------------------
# Memory Patterns
# Mike Christle 2022
# ---------------------------------------------------------------------------

import sys
import pygame
import state

from paint import paint, paint_intro, paint_background, get_xy
from logic import set_pattern, click

# 0.5 Second timer event
pygame.time.set_timer(pygame.USEREVENT, 500)

paint_intro()
delay_count = 0

while True:

    # Get all pygame events
    for event in pygame.event.get():
        match event.type:

            # Exit if window is closed
            case pygame.QUIT:
                sys.exit()

            # Any click starts the game
            case pygame.MOUSEBUTTONDOWN if state.state == state.ST_INTRO:
                state.state = state.ST_SHOW
                state.round = 0
                state.level = 0
                delay_count = 5

            # Wait for player to click on tiles
            case pygame.MOUSEBUTTONDOWN if state.state == state.ST_WAIT:
                x, y = get_xy(event.pos)
                click(x, y)

            # Delay 5 seconds then start a new game
            case pygame.USEREVENT if state.state == state.ST_SHOW:
                if delay_count == 0:
                    state.state = state.ST_WAIT
                    delay_count = 10
                    paint()
                if delay_count == 5:
                    state.round += 1
                    set_pattern()
                delay_count -= 1
