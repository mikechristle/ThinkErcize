# ---------------------------------------------------------------------------
# ThinkErcise, Logic
# Mike Christle 2022
# ---------------------------------------------------------------------------

import state as st

from random import randrange
from make_route import make_route
from paint import init_tracks, paint_btns
from enum_types import FuncT, DirT

last_color = 0
train_count = 0


# ---------------------------------------------------------------------------
def start_game():
    """Initialize and start a new game."""

    global train_count

    train_count = st.difficulty_level * 4
    st.total_trains = train_count
    st.game_score = 0
    make_route()
    init_tracks()
    st.game_active = True


# ---------------------------------------------------------------------------
def click_switch(x, y):
    """If the player clicks on a switch, toggle its st."""

    cell = st.grid[y][x]
    if cell is not None and cell[0] == FuncT.SWITCH:
        idx = cell[1]
        st.switches[idx][4] = not st.switches[idx][4]


# ---------------------------------------------------------------------------
def move_trains():
    """Move each train along the tracks."""

    # If there are no more trains, the game is over
    if train_count == 0 and len(st.trains) == 0:
        st.game_active = False
        paint_btns()

    # For each currently active train
    for _ in range(len(st.trains)):
        x, y, color = st.trains.pop(0)
        cell = st.grid[y][x]
        if cell is None:
            raise Exception(f'Train went off of the tracks at ({x}, {y})!')

        # Determine what type of track the train is on
        # Then move the train accordingly
        match cell:
            case [FuncT.TUNNEL | FuncT.TRACK, direction]:
                match direction:
                    case DirT.UP: y -= 1
                    case DirT.DOWN: y += 1
                    case DirT.RIGHT: x += 1
                    case DirT.LEFT: x -= 1
                st.trains.append((x, y, color))

            case [FuncT.TURN, direction, _]:
                match direction:
                    case DirT.UP: y -= 1
                    case DirT.DOWN: y += 1
                    case DirT.RIGHT: x += 1
                    case DirT.LEFT: x -= 1
                st.trains.append((x, y, color))

            case [FuncT.SWITCH, idx]:
                _, _, dir0, dir1, flag = st.switches[idx]
                direction = dir1 if flag else dir0
                match direction:
                    case DirT.UP: y -= 1
                    case DirT.DOWN: y += 1
                    case DirT.RIGHT: x += 1
                    case DirT.LEFT: x -= 1
                st.trains.append((x, y, color))

            case [FuncT.BARN, _, barn_color]:
                if color == barn_color:
                    st.game_score += 1


# ---------------------------------------------------------------------------
def add_trains():
    """
    Add a new train to the tunnel.
    Make sure each train does not have same color as last train.
    """

    global last_color, train_count

    if train_count > 0:
        while True:
            color = randrange(st.difficulty_level)
            if color != last_color:
                st.trains.append((st.tunnel_x, st.tunnel_y, color))
                train_count -= 1
                last_color = color
                break
