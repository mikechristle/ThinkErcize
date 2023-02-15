# ---------------------------------------------------------------------------
# Best Route
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame as py
import state as st

from sys import exit
from paint import paint, show_intro, build_background,\
                  get_xy, get_level, paint_status
from logic import start_game, click
from make_maze import make_maze
from shortest_route import find_shortest_route

show_intro()

while True:

    # Get all pygame events
    for event in py.event.get():
        match [event.type, st.state]:

            # Exit if window is closed
            case [py.QUIT, _]:
                exit()

            # Any click exits the intro
            case [py.MOUSEBUTTONDOWN, st.ST_INTRO]:
                st.state = st.ST_IDLE
                make_maze(st.grid_size, st.maze)
                build_background()
                paint()
                paint_status()

            # Change game level, or start a game
            case [py.MOUSEBUTTONDOWN, st.ST_IDLE]:
                level = get_level(event.pos)
                if level == 10:
                    st.state = st.ST_PLAY
                    start_game()
                    build_background()
                    find_shortest_route()
                    paint()
                elif 3 <= level <= 6:
                    st.level = level
                    st.grid_size = level + 2
                    paint_status()

            # Check each player click
            case [py.MOUSEBUTTONDOWN, st.ST_PLAY]:
                x, y = get_xy(event.pos)
                click(x, y)
                paint()
                if st.state == st.ST_IDLE:
                    paint_status()
