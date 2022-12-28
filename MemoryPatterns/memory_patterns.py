# ---------------------------------------------------------------------------
# Memory Patterns
# Mike Christle 2022
# ---------------------------------------------------------------------------

import sys
import pygame
import state as st

from paint import paint, paint_intro, paint_background, get_xy, paint_count
from logic import set_pattern, click

# 0.5 Second timer event
pygame.time.set_timer(pygame.USEREVENT, 500)

paint_intro()
delay_count = 0

while True:

    # Get all pygame events
    for event in pygame.event.get():
        match event.type:

            # Exit if window is closed
            case pygame.QUIT:
                sys.exit()

            # Any click starts the game
            case pygame.MOUSEBUTTONDOWN if st.state == st.ST_INTRO:
                st.state = st.ST_SHOW
                st.round = 0
                st.level = 0
                delay_count = 14

            # Wait for player to click on tiles
            case pygame.MOUSEBUTTONDOWN if st.state == st.ST_WAIT:
                x, y = get_xy(event.pos)
                click(x, y)
                paint()

            # Delay 5 seconds then start a new game
            case pygame.USEREVENT if st.state == st.ST_SHOW:
                match delay_count:
                    case 11:
                        paint_count('3')
                    case 9:
                        paint_count('2')
                    case 7:
                        paint_count('1')
                    case 5:
                        st.round += 1
                        set_pattern()
                        paint_background()
                        paint()
                    case 0:
                        st.state = st.ST_WAIT
                        delay_count = 20
                        paint()
                delay_count -= 1
