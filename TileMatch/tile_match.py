# ---------------------------------------------------------------------------
# Tile Match
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame as pg
import state as st

from time import time
from paint import paint, get_xy, show_intro, init_tiles
from logic import start_game, pick_new_tile, click, clear_grid

# 1.0 Second timer event
pg.time.set_timer(pg.USEREVENT, 1000)

start_time = 0

show_intro()
init_tiles()

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
                pick_new_tile()
                st.state = st.ST_START
                st.delay_count = 5

            # Process clicks during the game
            case [pg.MOUSEBUTTONDOWN, st.ST_PLAY]:
                x, y = get_xy(event.pos)
                if click(x, y) and st.state == st.ST_PLAY:
                    pick_new_tile()
                elif st.state == st.ST_IDLE:
                    st.run_time = round(time() - start_time, 1)
                    clear_grid()
                paint()

            # Display a count down timer to start a game
            case [pg.USEREVENT, st.ST_START]:
                st.delay_count -= 1
                if st.delay_count == 0:
                    start_time = time()
                    st.state = st.ST_PLAY
                if st.delay_count < 4:
                    paint()
