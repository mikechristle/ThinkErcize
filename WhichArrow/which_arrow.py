# ---------------------------------------------------------------------------
# Which Arrow
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame as pg
import state as st

from paint import paint, paint_intro

DECODER = {
    pg.K_UP: 0,
    pg.K_RIGHT: 1,
    pg.K_DOWN: 2,
    pg.K_LEFT: 3,
}

# Initialize window with instructions
paint_intro()

# 1.0 Second timer event for 45 second game timer
pg.time.set_timer(pg.USEREVENT, 1000)
timer = 0

while True:

    # Get all pygame events
    for event in pg.event.get():
        match event.type:

            # Exit if window is closed
            case pg.QUIT:
                exit()

            # Start new game if space bar pressed
            case pg.KEYDOWN if not st.game_active:
                if event.key == pg.K_SPACE:
                    st.score = 0
                    st.total = 0
                    st.game_active = True
                    timer = 45
                    paint()

            # Process arrow keys
            case pg.KEYDOWN if st.game_active:
                arrow = DECODER.get(event.key, 99)
                if arrow == st.main_arrow:
                    st.score += 1
                st.total += 1
                paint()

            # End of game timer
            case pg.USEREVENT:
                timer -= 1
                if timer == 0:
                    st.game_active = False
                    paint()
