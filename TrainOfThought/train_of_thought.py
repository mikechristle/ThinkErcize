# ---------------------------------------------------------------------------
# ThinkErcise
# Mike Christle 2022
# ---------------------------------------------------------------------------

import sys
import pygame
import state

from paint import paint, paint_btns, get_xy, paint_intro
from logic import click_switch, add_trains, move_trains, start_game

add_train_cntr = 0

# Initialize window with instructions
paint_btns()
paint_intro()
paint()

# 0.5 Second timer event to move trains
pygame.time.set_timer(pygame.USEREVENT, 500)

while True:

    # Get all pygame events
    for event in pygame.event.get():
        match event.type:

            # Exit if window is closed
            case pygame.QUIT:
                sys.exit()

            # If game active and clicked on game image,
            # check for a switch.
            case pygame.MOUSEBUTTONDOWN if state.game_active:
                x, y = get_xy(event.pos)
                if y < state.GRID_HEIGHT:
                    click_switch(x, y)
                    paint()

            # If game not active and clock on button bar,
            # check for buttons.
            case pygame.MOUSEBUTTONDOWN if not state.game_active:
                x, y = get_xy(event.pos)
                if y == state.GRID_HEIGHT:
                    if x < 6:
                        state.difficulty_level = x + 3
                        paint_btns()
                    elif x > (state.GRID_WIDTH - 5):
                        start_game()
                    paint()

            # On each timer tick move trains
            # Every fourth tick, add a new train
            case pygame.USEREVENT if state.game_active:
                move_trains()
                if add_train_cntr == 0:
                    add_train_cntr = 4
                    add_trains()
                else:
                    add_train_cntr -= 1
                paint()
