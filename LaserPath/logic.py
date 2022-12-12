# ---------------------------------------------------------------------------
# Laser Path, Logic
# Mike Christle 2022
# ---------------------------------------------------------------------------

import random
import state

from paint import laser_path, laser_path_append
from random import randrange

MIRRORS = (state.MIRROR1, state.MIRROR2)
LASER_LOCS = (
    (0, 1, state.LASER_E), (0, 2, state.LASER_E), (0, 3, state.LASER_E),
    (0, 4, state.LASER_E), (0, 5, state.LASER_E), (1, 0, state.LASER_S),
    (2, 0, state.LASER_S), (3, 0, state.LASER_S), (4, 0, state.LASER_S),
    (5, 0, state.LASER_S), (6, 1, state.LASER_W), (6, 2, state.LASER_W),
    (6, 3, state.LASER_W), (6, 4, state.LASER_W), (6, 5, state.LASER_W),
    (1, 6, state.LASER_N), (2, 6, state.LASER_N), (3, 6, state.LASER_N),
    (4, 6, state.LASER_N), (5, 6, state.LASER_N)
)

exit_x = 0
exit_y = 0


# ---------------------------------------------------------------------------
def start_game():
    """Start of a game of ten rounds."""

    state.mirrors = 4
    state.round = 1
    state.score = 0


# ---------------------------------------------------------------------------
def start_round():
    """Start of a round."""

    set_mirrors()
    set_laser()


# ---------------------------------------------------------------------------
def set_laser():
    """Position a laser so that the beam hits at least one mirror."""

    while True:

        # Select a random laser location
        x, y, d = random.choice(LASER_LOCS)

        # Trace the path from this location
        state.grid[y][x] = d
        count = get_path(x, y, d)

        # Laser beam must hit at least one mirror
        if count > 0:
            return
        else:
            state.grid[y][x] = state.EMPTY


# ---------------------------------------------------------------------------
def get_path(x, y, d):
    """
    Determine the path of the laser beam.
    x, y   Current location of beam
    d      Direction beam is traveling
    """

    global exit_x, exit_y

    mirror_count = 0
    laser_path.clear()

    while True:

        # Save the current location
        laser_path_append(x, y)

        # Count how many mirrors are hit
        cell = state.grid[y][x]
        if cell == state.MIRROR1 or cell == state.MIRROR2:
            mirror_count += 1

        # Move location to the next cell
        match [d, cell]:
            case [state.LASER_N, state.MIRROR1]:
                x += 1
                d = state.LASER_E
            case [state.LASER_S, state.MIRROR1]:
                x -= 1
                d = state.LASER_W
            case [state.LASER_E, state.MIRROR1]:
                y -= 1
                d = state.LASER_N
            case [state.LASER_W, state.MIRROR1]:
                y += 1
                d = state.LASER_S
            case [state.LASER_N, state.MIRROR2]:
                x -= 1
                d = state.LASER_W
            case [state.LASER_S, state.MIRROR2]:
                x += 1
                d = state.LASER_E
            case [state.LASER_E, state.MIRROR2]:
                y += 1
                d = state.LASER_S
            case [state.LASER_W, state.MIRROR2]:
                y -= 1
                d = state.LASER_N
            case [state.LASER_N, _]:
                y -= 1
            case [state.LASER_S, _]:
                y += 1
            case [state.LASER_E, _]:
                x += 1
            case [state.LASER_W, _]:
                x -= 1

        # If laser beam exits playing area,
        # save exit location and return mirror count.
        if x == 0 or x == 6 or y == 0 or y == 6:
            laser_path_append(x, y)
            exit_x = x
            exit_y = y
            return mirror_count


# ---------------------------------------------------------------------------
def set_mirrors():
    """Randomly position mirrors."""

    # Clear all mirrors and laser cannons from previous round
    for line in state.grid:
        for x in range(7):
            line[x] = state.EMPTY

    # Loop until enough mirrors are places on grid
    count = state.mirrors
    while count > 0:
        x = randrange(1, 6)
        y = randrange(1, 6)
        if state.grid[y][x] == state.EMPTY:
            state.grid[y][x] = random.choice(MIRRORS)
            count -= 1


# ---------------------------------------------------------------------------
def check_click(x, y):
    """Determine if the selected exit matches the laser beams exit."""

    if ((x == 0 or x == 6) and (0 < y < 6)) or \
       ((y == 0 or y == 6) and (0 < x < 6)):

        state.click_x = x
        state.click_y = y

        if x == exit_x and y == exit_y:
            state.score += state.mirrors
            state.mirrors += 1
        elif state.mirrors > 4:
            state.mirrors -= 1
        return True
    else:
        return False
