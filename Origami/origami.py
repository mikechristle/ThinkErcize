# ---------------------------------------------------------------------------
# Origami
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame
import state as st

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
        match event.type:

            # Exit if window is closed
            case pygame.QUIT:
                exit()

            # Any click starts the game
            case pygame.MOUSEBUTTONDOWN if st.state == st.ST_IDLE:
                st.state = st.ST_WAIT
                set_pattern()
                paint()

            # Move the cursor over the image
            case pygame.MOUSEMOTION if st.state == st.ST_WAIT:
                x, y = get_xy(event.pos)
                if x >= 0:
                    st.cursor_x = x
                    st.cursor_y = y
                    paint()

            # Player selects a position
            case pygame.MOUSEBUTTONDOWN if st.state == st.ST_WAIT:
                if check_click():
                    paint()
                    delay_count = 10
                    st.state = st.ST_DONE

            # Delay 5 seconds then start a new game
            case pygame.USEREVENT if st.state == st.ST_DONE:
                delay_count -= 1
                if delay_count == 0:
                    st.state = st.ST_WAIT
                    set_pattern()
                    paint()
