# ---------------------------------------------------------------------------
# Digit Order
# A memory development game.
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame as pg
import state as st

from sys import exit
from paint import paint, get_xy, show_intro, paint_count
from logic import start_game, start_cycle, click

# 0.25 Second timer event
pg.time.set_timer(pg.USEREVENT, 250)

show_intro()
delay_count = 0

while True:

    # Get all pygame events
    for event in pg.event.get():
        match [event.type, st.state]:

            # Exit if window is closed
            case [pg.QUIT, _]:
                exit()

            # Any click starts the game
            case [pg.MOUSEBUTTONDOWN, st.ST_IDLE]:
                start_game()
                st.state = st.ST_NEXT
                delay_count = 1
                # paint()

            # Delay before starting next round
            case [pg.USEREVENT, st.ST_NEXT]:
                if st.cycle == 10:
                    st.state = st.ST_IDLE
                    paint()
                else:
                    delay_count -= 1
                    if delay_count == 0:
                        st.cycle += 1
                        st.state = st.ST_SHOW
                        delay_count = 46

            # Timer event generated delays
            case [pg.USEREVENT, st.ST_SHOW]:
                delay_count -= 1
                match delay_count:
                    case 44:
                        paint_count('3')
                    case 40:
                        paint_count('2')
                    case 36:
                        paint_count('1')
                    case 32:
                        delay_count = 4 + st.count
                        start_cycle()
                        paint()
                    case 0:
                        st.state = st.ST_WAIT
                        delay_count = 16
                        paint()

            # Check each player click
            case [pg.MOUSEBUTTONDOWN, st.ST_WAIT]:
                x, y = get_xy(event.pos)
                click(x, y)
                paint()
