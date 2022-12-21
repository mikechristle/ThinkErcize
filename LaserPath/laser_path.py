# ---------------------------------------------------------------------------
# Laser Path
# A memory development game.
# Mike Christle 2022
# ---------------------------------------------------------------------------

import sys
import pygame
import state as st

from paint import paint, get_xy, show_intro, update_status, new_game
from logic import start_game, start_round, check_click

# 1.0 Second timer event
pygame.time.set_timer(pygame.USEREVENT, 1000)

show_intro()
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
            case pygame.MOUSEBUTTONDOWN if st.state == st.ST_IDLE:
                start_game()
                st.state = st.ST_START

            # Player selects an exit square
            case pygame.MOUSEBUTTONDOWN if st.state == st.ST_WAIT:
                x, y = get_xy(event.pos)
                if check_click(x, y):
                    st.state = st.ST_FIRE
                    delay_count = 6
                    paint()
                    st.state = st.ST_DONE

            # Start a new round
            case pygame.USEREVENT if st.state == st.ST_START:
                start_round()
                update_status()
                paint()
                st.state = st.ST_COUNT3

            # Three second countdown
            case pygame.USEREVENT if st.state == st.ST_COUNT3:
                paint()
                st.state = st.ST_COUNT2

            case pygame.USEREVENT if st.state == st.ST_COUNT2:
                paint()
                st.state = st.ST_COUNT1

            case pygame.USEREVENT if st.state == st.ST_COUNT1:
                paint()
                delay_count = 4
                st.state = st.ST_SHOW

            # Show the mirrors for 5 seconds
            case pygame.USEREVENT if st.state == st.ST_SHOW:
                paint()
                if delay_count == 0:
                    st.state = st.ST_WAIT
                    paint()
                delay_count -= 1

            # End of a round
            case pygame.USEREVENT if st.state == st.ST_DONE:
                if st.cycle < 10:
                    delay_count -= 1
                    if delay_count <= 0:
                        st.cycle += 1
                        st.state = st.ST_START
                else:
                    new_game()
                    st.state = st.ST_IDLE

