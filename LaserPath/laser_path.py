# ---------------------------------------------------------------------------
# Laser Path
# A memory development game.
# Mike Christle 2022
# ---------------------------------------------------------------------------

import sys
import pygame
import state

from paint import paint, init_background, get_xy, show_intro, update_status, new_game
from logic import start_game, start_round, check_click

# 1.0 Second timer event
pygame.time.set_timer(pygame.USEREVENT, 1000)

show_intro()
init_background()
update_status()

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
                start_game()
                state.state = state.ST_START

            # Player selects an exit square
            case pygame.MOUSEBUTTONDOWN if state.state == state.ST_WAIT:
                x, y = get_xy(event.pos)
                if check_click(x, y):
                    state.state = state.ST_FIRE
                    delay_count = 6
                    paint()
                    state.state = state.ST_DONE

            # Start a new round
            case pygame.USEREVENT if state.state == state.ST_START:
                start_round()
                update_status()
                paint()
                state.state = state.ST_COUNT3

            # Three second countdown
            case pygame.USEREVENT if state.state == state.ST_COUNT3:
                paint()
                state.state = state.ST_COUNT2

            case pygame.USEREVENT if state.state == state.ST_COUNT2:
                paint()
                state.state = state.ST_COUNT1

            case pygame.USEREVENT if state.state == state.ST_COUNT1:
                paint()
                delay_count = 4
                state.state = state.ST_SHOW

            # Show the mirrors for 5 seconds
            case pygame.USEREVENT if state.state == state.ST_SHOW:
                paint()
                if delay_count == 0:
                    state.state = state.ST_WAIT
                    paint()
                delay_count -= 1

            # End of a round
            case pygame.USEREVENT if state.state == state.ST_DONE:
                if state.round < 10:
                    delay_count -= 1
                    if delay_count <= 0:
                        state.round += 1
                        state.state = state.ST_START
                else:
                    new_game()
                    state.state = state.ST_IDLE

