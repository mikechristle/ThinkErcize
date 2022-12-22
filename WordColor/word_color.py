# ---------------------------------------------------------------------------
# Word Color
# Mike Christle 2022
# ---------------------------------------------------------------------------

import sys
import pygame
import state as st

from paint import paint, paint_intro
from logic import start_round, check

timeout_counter = 0

# Initialize window with instructions
paint_intro()

# 1.0 Second timer event
pygame.time.set_timer(pygame.USEREVENT, 1000)

while True:

    # Get all pygame events
    for event in pygame.event.get():
        match event.type:

            # Exit if window is closed
            case pygame.QUIT:
                sys.exit()

            # Pressing the space ber starts a round
            case pygame.KEYDOWN if not st.game_active:
                if event.key == pygame.K_SPACE:
                    start_round()
                    timeout_counter = 30
                    paint()

            # Right and left arrow keys for player input
            case pygame.KEYDOWN if st.game_active:
                if event.key == pygame.K_LEFT or \
                   event.key == pygame.K_RIGHT:
                    check(event.key)
                    paint()

            # Thirty second round timer
            case pygame.USEREVENT if st.game_active:
                timeout_counter -= 1
                if timeout_counter == 0:
                    st.game_active = False
                    paint()
