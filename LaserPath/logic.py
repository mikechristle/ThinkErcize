# ---------------------------------------------------------------------------
# Laser Path, Logic
# Mike Christle 2022
# ---------------------------------------------------------------------------

import state as st

from paint import laser_path, laser_path_append
from random import randrange, choice

MIRRORS = (st.MIRROR1, st.MIRROR2)
LASER_LOCS = (
    (0, 1, st.LASER_E), (0, 2, st.LASER_E), (0, 3, st.LASER_E),
    (0, 4, st.LASER_E), (0, 5, st.LASER_E), (1, 0, st.LASER_S),
    (2, 0, st.LASER_S), (3, 0, st.LASER_S), (4, 0, st.LASER_S),
    (5, 0, st.LASER_S), (6, 1, st.LASER_W), (6, 2, st.LASER_W),
    (6, 3, st.LASER_W), (6, 4, st.LASER_W), (6, 5, st.LASER_W),
    (1, 6, st.LASER_N), (2, 6, st.LASER_N), (3, 6, st.LASER_N),
    (4, 6, st.LASER_N), (5, 6, st.LASER_N)
)

exit_x = 0
exit_y = 0


# ---------------------------------------------------------------------------
def start_game():
    """Start of a game of ten rounds."""

    st.mirrors = 4
    st.cycle = 1
    st.score = 0


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
        x, y, d = choice(LASER_LOCS)

        # Trace the path from this location
        st.grid[y][x] = d
        count = get_path(x, y, d)

        # Laser beam must hit at least one mirror
        if count > 0:
            return
        else:
            st.grid[y][x] = st.EMPTY


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
        cell = st.grid[y][x]
        if cell == st.MIRROR1 or cell == st.MIRROR2:
            mirror_count += 1

        # Move location to the next cell
        match [d, cell]:
            case [st.LASER_N, st.MIRROR1]:
                x += 1
                d = st.LASER_E
            case [st.LASER_S, st.MIRROR1]:
                x -= 1
                d = st.LASER_W
            case [st.LASER_E, st.MIRROR1]:
                y -= 1
                d = st.LASER_N
            case [st.LASER_W, st.MIRROR1]:
                y += 1
                d = st.LASER_S
            case [st.LASER_N, st.MIRROR2]:
                x -= 1
                d = st.LASER_W
            case [st.LASER_S, st.MIRROR2]:
                x += 1
                d = st.LASER_E
            case [st.LASER_E, st.MIRROR2]:
                y += 1
                d = st.LASER_S
            case [st.LASER_W, st.MIRROR2]:
                y -= 1
                d = st.LASER_N
            case [st.LASER_N, _]:
                y -= 1
            case [st.LASER_S, _]:
                y += 1
            case [st.LASER_E, _]:
                x += 1
            case [st.LASER_W, _]:
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
    for line in st.grid:
        for x in range(7):
            line[x] = st.EMPTY

    # Loop until enough mirrors are places on grid
    count = st.mirrors
    while count > 0:
        x = randrange(1, 6)
        y = randrange(1, 6)
        if st.grid[y][x] == st.EMPTY:
            st.grid[y][x] = choice(MIRRORS)
            count -= 1


# ---------------------------------------------------------------------------
def check_click(x, y):
    """Determine if the selected exit matches the laser beams exit."""

    if ((x == 0 or x == 6) and (0 < y < 6)) or \
       ((y == 0 or y == 6) and (0 < x < 6)):

        st.click_x = x
        st.click_y = y

        if x == exit_x and y == exit_y:
            st.score += st.mirrors
            st.mirrors += 1
        elif st.mirrors > 4:
            st.mirrors -= 1
        return True
    else:
        return False
