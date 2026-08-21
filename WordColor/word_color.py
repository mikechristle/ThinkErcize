# ---------------------------------------------------------------------------
# Word Color
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame as pg
import state as st

from paint import paint, paint_intro
from logic import start_round, check
from time import time


# Initialize window with instructions
paint_intro()

while True:

    # Get all pygame events
    for event in pg.event.get():
        match event.type:

            # Exit if window is closed
            case pg.QUIT:
                exit()

            # Pressing the space ber starts a round
            case pg.KEYDOWN if not st.game_active:
                if event.key == pg.K_SPACE:
                    start_round()
                    st.run_time = time()
                    paint()

            # Right and left arrow keys for player input
            case pg.KEYDOWN if st.game_active:
                if event.key == pg.K_LEFT or \
                   event.key == pg.K_RIGHT:
                    check(event.key)
                    if st.total == 25:
                        st.run_time = time() - st.run_time
                        st.game_active = False
                        print(f'word_color {st.score} {st.run_time:.1f}')
                    paint()
