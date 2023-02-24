# ---------------------------------------------------------------------------
# Word Color
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame as pg
import state as st

from paint import paint, paint_intro
from logic import start_round, check

timeout_counter = 0

# Initialize window with instructions
paint_intro()

# 1.0 Second timer event
pg.time.set_timer(pg.USEREVENT, 1000)

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
                    timeout_counter = 30
                    paint()

            # Right and left arrow keys for player input
            case pg.KEYDOWN if st.game_active:
                if event.key == pg.K_LEFT or \
                   event.key == pg.K_RIGHT:
                    check(event.key)
                    paint()

            # Thirty second round timer
            case pg.USEREVENT if st.game_active:
                timeout_counter -= 1
                if timeout_counter == 0:
                    st.game_active = False
                    paint()
