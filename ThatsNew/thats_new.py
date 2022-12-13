# ---------------------------------------------------------------------------
# That's New
# A memory enhancement game.
# Mike Christle 2022
# ---------------------------------------------------------------------------

import sys
import pygame
import state

from paint import paint, get_xy, paint_intro
from logic import init_game, click


# Display the intro screen
paint_intro()

while True:

    # Get all pygame events
    for event in pygame.event.get():
        match event.type:

            # Exit if window is closed
            case pygame.QUIT:
                sys.exit()

            # Process clicks on images
            case pygame.MOUSEBUTTONDOWN if state.game_active:
                x, y = get_xy(event.pos)
                click(x, y)
                paint()

            # Any click starts a new game
            case pygame.MOUSEBUTTONDOWN if not state.game_active:
                init_game()
                paint()
