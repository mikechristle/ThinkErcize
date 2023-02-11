# ---------------------------------------------------------------------------
# Who Am I
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame
import state as st

from sys import exit
from paint import paint, paint_status
from logic import start_game, start_round, show_image, check


# 1.0 Second timer event
pygame.time.set_timer(pygame.USEREVENT, 1000)

paint()
start_game()

while True:

    # Get all pygame events
    for event in pygame.event.get():
        match [event.type, st.state]:

            # Exit if window is closed
            case [pygame.QUIT, _]:
                exit()

            # Any click starts the game
            case [pygame.MOUSEBUTTONDOWN, st.ST_INTRO]:
                st.state = st.ST_COUNT
                st.delay = 5
                paint_status(0)

            case [pygame.USEREVENT, st.ST_SHOW]:
                st.delay -= 1
                if st.delay == 0:
                    show_image()
                    st.delay = 4

            # Player selects a position
            case [pygame.MOUSEBUTTONDOWN, st.ST_WAIT]:
                check(event.pos)

            # Delay 5 seconds then start a new game
            case [pygame.USEREVENT, st.ST_COUNT]:
                st.delay -= 1
                if 4 > st.delay > 0:
                    paint_status(st.delay)
                elif st.delay == 0:
                    st.delay = 4
                    st.state = st.ST_SHOW
                    start_round()
                    show_image()
