# ---------------------------------------------------------------------------
# Train of Thought
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame as pg
import state as st

from paint import paint, paint_btns, get_xy, paint_intro
from logic import click_switch, add_trains, move_trains, start_game

add_train_cntr = 0

# Initialize window with instructions
paint_btns()
paint_intro()
paint()

# 0.5 Second timer event to move trains
pg.time.set_timer(pg.USEREVENT, 500)

while True:

    # Get all pygame events
    for event in pg.event.get():
        match event.type:

            # Exit if window is closed
            case pg.QUIT:
                exit()

            # If game active and clicked on game image,
            # check for a switch.
            case pg.MOUSEBUTTONDOWN if st.game_active:
                x, y = get_xy(event.pos)
                if y < st.GRID_HEIGHT:
                    click_switch(x, y)
                    paint()

            # If game not active and clock on button bar,
            # check for buttons.
            case pg.MOUSEBUTTONDOWN if not st.game_active:
                x, y = get_xy(event.pos)
                if y == st.GRID_HEIGHT:
                    if x < 6:
                        st.difficulty_level = x + 3
                        paint_btns()
                    elif x > (st.GRID_WIDTH - 5):
                        start_game()
                    paint()

            # On each timer tick move trains
            # Every fourth tick, add a new train
            case pg.USEREVENT if st.game_active:
                move_trains()
                if add_train_cntr == 0:
                    add_train_cntr = 4
                    add_trains()
                else:
                    add_train_cntr -= 1
                paint()
