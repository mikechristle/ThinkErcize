# ---------------------------------------------------------------------------
# Tile Match
# Mike Christle 2022
# ---------------------------------------------------------------------------

import time
import pygame
import state as st

from sys import exit
from paint import paint, get_xy, show_intro, init_tiles
from logic import start_game, pick_new_tile, click, clear_grid

# 1.0 Second timer event
pygame.time.set_timer(pygame.USEREVENT, 1000)

start_time = 0

show_intro()
init_tiles()

while True:

    # Get all pygame events
    for event in pygame.event.get():
        match event.type:

            # Exit if window is closed
            case pygame.QUIT:
                exit()

            # Any click starts the game
            case pygame.MOUSEBUTTONDOWN if st.state == st.ST_IDLE:
                start_game()
                pick_new_tile()
                st.state = st.ST_START
                st.delay_count = 5

            # Process clicks during the game
            case pygame.MOUSEBUTTONDOWN if st.state == st.ST_PLAY:
                x, y = get_xy(event.pos)
                if click(x, y) and st.state == st.ST_PLAY:
                    pick_new_tile()
                elif st.state == st.ST_IDLE:
                    st.run_time = round(time.time() - start_time, 1)
                    clear_grid()
                paint()

            # Display a count down timer to start a game
            case pygame.USEREVENT if st.state == st.ST_START:
                st.delay_count -= 1
                if st.delay_count == 0:
                    start_time = time.time()
                    st.state = st.ST_PLAY
                if st.delay_count < 4:
                    paint()
