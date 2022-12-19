# ---------------------------------------------------------------------------
# Memory Patterns
# Game Logic
# Mike Christle 2022
# ---------------------------------------------------------------------------

import state
from random import randrange
from paint import paint, paint_background

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
            state.grid[y][x] = state.BLANK

    # Get the stats for the current level
    width, height, count = state.LEVELS[state.level]

    # Randomly fill tiles in the grid
    click_count = count
    error_count = 0
    while count > 0:
        x = randrange(width)
        y = randrange(height)
        if state.grid[y][x] == state.BLANK:
            state.grid[y][x] = state.TILE
            count -= 1

    # Update the background image
    paint_background()
    paint()


# ---------------------------------------------------------------------------
def click(x, y):
    """Check a players selection."""

    global click_count, error_count

    # Ignore clicks outside of the grid.
    if x < 0 or x >= width or y < 0 or y >= height:
        return

    # If cell is blank, report the error
    cell = state.grid[y][x]
    if cell == state.BLANK:
        cell = state.ERROR
        error_count += 1
        click_count -= 1

    # If cell is a tile, report success
    elif cell == state.TILE:
        cell = state.CLICK
        click_count -= 1

    # Update display
    state.grid[y][x] = cell
    paint()

    # End of round
    if click_count == 0:
        state.state = state.ST_SHOW
        paint()
        if error_count == 0 and state.level < 8:
            state.level += 1
        if state.round == 10:
            state.state = state.ST_INTRO
            paint()
