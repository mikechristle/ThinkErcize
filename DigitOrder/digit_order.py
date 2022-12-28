# ---------------------------------------------------------------------------
# Digit Order
# A memory development game.
# Mike Christle 2022
# ---------------------------------------------------------------------------

import sys
import pygame
import state as st

from paint import paint, get_xy, show_intro, paint_count
from logic import start_game, start_cycle, click

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
                sys.exit()

            # Any click starts the game
            case [pygame.MOUSEBUTTONDOWN, st.ST_IDLE]:
                start_game()
                st.state = st.ST_NEXT
                paint()

            # Delay before starting next round
            case [pygame.USEREVENT, st.ST_NEXT]:
                if st.cycle == 10:
                    st.state = st.ST_IDLE
                    paint()
                else:
                    st.cycle += 1
                    st.state = st.ST_SHOW
                    delay_count = 50

            # Timer event generated delays
            case [pygame.USEREVENT, st.ST_SHOW]:
                delay_count -= 1
                match delay_count:
                    case 42:
                        paint_count('3')
                    case 39:
                        paint_count('2')
                    case 36:
                        paint_count('1')
                    case 33:
                        delay_count = 4 + st.count
                        start_cycle()
                        paint()
                    case 0:
                        st.state = st.ST_WAIT
                        paint()

            # Check each player click
            case [pygame.MOUSEBUTTONDOWN, st.ST_WAIT]:
                x, y = get_xy(event.pos)
                click(x, y)
                paint()
