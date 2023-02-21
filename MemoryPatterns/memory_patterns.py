# ---------------------------------------------------------------------------
# Memory Patterns
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame as pg
import state as st

from sys import exit
from paint import paint, paint_intro, paint_background, get_xy, paint_count
from logic import set_pattern, click

# 0.5 Second timer event
pg.time.set_timer(pg.USEREVENT, 500)

paint_intro()
delay_count = 0

while True:

    # Get all pygame events
    for event in pg.event.get():
        match [event.type, st.state]:

            # Exit if window is closed
            case [pg.QUIT, _]:
                exit()

            # Any click starts the game
            case [pg.MOUSEBUTTONDOWN, st.ST_INTRO]:
                st.state = st.ST_COUNT
                st.cycle = 0
                st.level = 0
                st.score = 0
                delay_count = 12

            # Delay 5 seconds then start a new game
            case [pg.USEREVENT, st.ST_COUNT]:
                match delay_count:
                    case 11:
                        paint_count('3')
                    case 9:
                        paint_count('2')
                    case 7:
                        paint_count('1')
                    case 5:
                        st.cycle += 1
                        set_pattern()
                        paint_background()
                        paint()
                    case 0:
                        st.state = st.ST_WAIT
                        delay_count = 8
                        paint()
                delay_count -= 1

            # Wait for player to click on tiles
            case [pg.MOUSEBUTTONDOWN, st.ST_WAIT]:
                x, y = get_xy(event.pos)
                click(x, y)
                paint()

            # Show results of the round
            case [pg.USEREVENT, st.ST_SHOW]:
                delay_count -= 1
                if delay_count == 0:
                    st.state = st.ST_COUNT
                    delay_count =12
