# ---------------------------------------------------------------------------
# Laser Path
# A memory development game.
# Mike Christle 2022
# ---------------------------------------------------------------------------

import sys
import pygame
import state as st

from logic import start_game, start_round, check_click
from paint import paint, get_xy, show_intro, update_status, new_game,\
                  fire_laser, show_count

# 1.0 Second timer event
pygame.time.set_timer(pygame.USEREVENT, 1000)

delay_count = 0
show_intro()

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
                delay_count = 5
                st.state = st.ST_START

            # Start a new round
            case [pygame.USEREVENT, st.ST_START]:
                start_round()
                update_status()
                paint()
                delay_count -= 1
                match delay_count:
                    case 3:
                        show_count('3')
                    case 2:
                        show_count('2')
                    case 1:
                        show_count('1')
                        delay_count = 4
                        st.state = st.ST_SHOW

            # Show the mirrors for 5 seconds
            case [pygame.USEREVENT, st.ST_SHOW]:
                paint()
                if delay_count == 0:
                    st.state = st.ST_WAIT
                    paint()
                delay_count -= 1

            # Player selects an exit square
            case [pygame.MOUSEBUTTONDOWN, st.ST_WAIT]:
                x, y = get_xy(event.pos)
                if check_click(x, y):
                    fire_laser()
                    delay_count = 6
                    st.state = st.ST_DONE

            # End of a round
            case [pygame.USEREVENT, st.ST_DONE]:
                if st.cycle < 10:
                    delay_count -= 1
                    if delay_count <= 0:
                        st.cycle += 1
                        delay_count = 5
                        st.state = st.ST_START
                else:
                    new_game()
                    st.state = st.ST_IDLE

