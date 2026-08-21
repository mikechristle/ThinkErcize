# ---------------------------------------------------------------------------
# Which Arrow
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame as pg
import state as st

from paint import paint, paint_intro
from time import time

DECODER = {
    pg.K_UP: 0,
    pg.K_RIGHT: 1,
    pg.K_DOWN: 2,
    pg.K_LEFT: 3,
}

# Initialize window with instructions
paint_intro()

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
                    st.run_time = time()
                    st.game_active = True
                    timer = 45
                    paint()

            # Process arrow keys
            case pg.KEYDOWN if st.game_active:
                arrow = DECODER.get(event.key, 99)
                if arrow == st.main_arrow:
                    st.score += 1
                st.total += 1
                if st.total == 100:
                    st.run_time = time() - st.run_time
                    st.game_active = False
                    print(f'which_arrow {st.score} {st.run_time:.1f}')
                paint()
