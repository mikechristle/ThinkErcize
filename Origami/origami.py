# ---------------------------------------------------------------------------
# Origami
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame
import state as st

from time import time
from sys import exit
from paint import paint, get_xy, show_intro
from logic import set_pattern, check_click

# 0.25 Second timer event
pygame.time.set_timer(pygame.USEREVENT, 250)

show_intro()
delay_count = 0

while True:

    # Get all pygame events
    for event in pygame.event.get():
        match [event.type, st.state]:

            # Exit if window is closed
            case [pygame.QUIT, _]:
                exit()

            # Any click starts the game
            case [pygame.MOUSEBUTTONDOWN, st.ST_IDLE]:
                st.state = st.ST_WAIT
                st.games = 0
                st.score = 0
                st.start_time = time()
                set_pattern()
                paint()

            # Move the cursor over the image
            case [pygame.MOUSEMOTION, st.ST_WAIT]:
                x, y = get_xy(event.pos)
                st.cursor_x = x
                st.cursor_y = y
                paint()

            # Player selects a position
            case [pygame.MOUSEBUTTONDOWN, st.ST_WAIT]:
                if check_click():
                    paint()
                    delay_count = 10
                    if st.games == 10:
                        st.start_time = time() - st.start_time
                        st.state = st.ST_IDLE
                        paint()
                    else:
                        st.state = st.ST_DONE

            # Delay 5 seconds then start a new game
            case [pygame.USEREVENT, st.ST_DONE]:
                delay_count -= 1
                if delay_count == 0:
                    st.state = st.ST_WAIT
                    set_pattern()
                    paint()
