# ---------------------------------------------------------------------------
# Best Route
# Mike Christle 2022
# ---------------------------------------------------------------------------

import sys
import pygame
import state as st

from paint import paint, show_intro, build_background,\
                  get_xy, get_level, paint_status
from logic import start_game, click
from make_maze import make_maze

show_intro()

while True:

    # Get all pygame events
    for event in pygame.event.get():
        match [event.type, st.state]:

            # Exit if window is closed
            case [pygame.QUIT, _]:
                sys.exit()

            # Any click exits the intro
            case [pygame.MOUSEBUTTONDOWN, st.ST_INTRO]:
                st.state = st.ST_IDLE
                make_maze(st.level, st.maze)
                build_background()
                paint()
                paint_status()

            # Change game level, or start a game
            case [pygame.MOUSEBUTTONDOWN, st.ST_IDLE]:
                level = get_level(event.pos)
                if level == 10:
                    st.state = st.ST_PLAY
                    start_game()
                    build_background()
                    paint()
                elif 4 <= level <= 8:
                    st.level = level
                    paint_status()

            # Check each player click
            case [pygame.MOUSEBUTTONDOWN, st.ST_PLAY]:
                x, y = get_xy(event.pos)
                click(x, y)
                paint()
                if st.state == st.ST_IDLE:
                    paint_status()
