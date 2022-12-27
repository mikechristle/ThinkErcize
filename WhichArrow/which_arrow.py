# ---------------------------------------------------------------------------
# Which Arrow
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame
import state as st

from sys import exit
from paint import paint, paint_intro

DECODER = {
    pygame.K_UP: 0,
    pygame.K_RIGHT: 1,
    pygame.K_DOWN: 2,
    pygame.K_LEFT: 3,
}

# Initialize window with instructions
paint_intro()

# 1.0 Second timer event for 45 second game timer
pygame.time.set_timer(pygame.USEREVENT, 1000)
timer = 0

while True:

    # Get all pygame events
    for event in pygame.event.get():
        match event.type:

            # Exit if window is closed
            case pygame.QUIT:
                exit()

            # Start new game if space bar pressed
            case pygame.KEYDOWN if not st.game_active:
                if event.key == pygame.K_SPACE:
                    st.score = 0
                    st.total = 0
                    st.game_active = True
                    timer = 45
                    paint()

            # Process arrow keys
            case pygame.KEYDOWN if st.game_active:
                arrow = DECODER.get(event.key, 99)
                if arrow == st.main_arrow:
                    st.score += 1
                st.total += 1
                paint()

            # End of game timer
            case pygame.USEREVENT:
                timer -= 1
                if timer == 0:
                    st.game_active = False
                    paint()
