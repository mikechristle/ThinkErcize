# ---------------------------------------------------------------------------
# Memory Patterns
# Game Logic
# Mike Christle 2022
# ---------------------------------------------------------------------------

import state as st

from random import randrange

click_count = 0
error_count = 0
width = 0
height = 0


# ---------------------------------------------------------------------------
def set_pattern():
    """Build a random pattern of tiles."""

    global click_count, error_count, width, height

    # Clear the grid
    for y in range(7):
        for x in range(7):
            st.grid[y][x] = st.BLANK

    # Get the stats for the current level
    width, height, count = st.LEVELS[st.level]

    # Randomly fill tiles in the grid
    click_count = count
    error_count = 0
    while count > 0:
        x = randrange(width)
        y = randrange(height)
        if st.grid[y][x] == st.BLANK:
            st.grid[y][x] = st.TILE
            count -= 1


# ---------------------------------------------------------------------------
def click(x, y):
    """Check a players selection."""

    global click_count, error_count

    # Ignore clicks outside of the grid.
    if x < 0 or x >= width or y < 0 or y >= height:
        return

    # If cell is blank, report the error
    cell = st.grid[y][x]
    if cell == st.BLANK:
        cell = st.ERROR
        error_count += 1
        click_count -= 1

    # If cell is a tile, report success
    elif cell == st.TILE:
        cell = st.CLICK
        click_count -= 1

    # Update display
    st.grid[y][x] = cell

    # End of round
    if click_count == 0:
        st.state = st.ST_SHOW
        if error_count == 0 and st.level < 8:
            st.level += 1
        if st.round == 10:
            st.state = st.ST_INTRO
