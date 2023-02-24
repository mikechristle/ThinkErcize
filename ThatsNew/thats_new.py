# ---------------------------------------------------------------------------
# That's New
# A memory enhancement game.
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame as pg
import state as st

from paint import paint, get_xy, paint_intro
from logic import init_game, click


# Display the intro screen
paint_intro()

while True:

    # Get all pygame events
    for event in pg.event.get():
        match event.type:

            # Exit if window is closed
            case pg.QUIT:
                exit()

            # Process clicks on images
            case pg.MOUSEBUTTONDOWN if st.game_active:
                x, y = get_xy(event.pos)
                click(x, y)
                paint()

            # Any click starts a new game
            case pg.MOUSEBUTTONDOWN if not st.game_active:
                init_game()
                paint()
