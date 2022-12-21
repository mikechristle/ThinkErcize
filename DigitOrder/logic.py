# ---------------------------------------------------------------------------
# Digit Order
# Mike Christle 2022
# ---------------------------------------------------------------------------

import state as st
from random import randrange, shuffle

last_value = 0
number_count = 0


# ---------------------------------------------------------------------------
def start_game():
    """Setup for a new game."""

    st.score = 0
    st.cycle = 1
    st.count = 4
    clear_grid()


# ---------------------------------------------------------------------------
def start_cycle():
    """Setup for a new round."""

    global last_value, number_count

    clear_grid()
    last_value = 0
    number_count = st.count

    nums = [x for x in range(1, 10)]
    shuffle(nums)
    count = st.count
    while count > 0:
        x = randrange(st.GRID_WIDTH)
        y = randrange(st.GRID_HEIGHT)
        cell = st.grid[y][x]
        if cell.state == st.BLANK:
            st.grid[y][x].value = nums.pop(0)
            st.grid[y][x].state = st.NUMBER
            count -= 1


# ---------------------------------------------------------------------------
def click(x, y):
    """Check a user click."""

    global last_value, number_count

    # Ignore clicks on the status bar
    if y >= st.GRID_HEIGHT:
        return

    # Ignore any cell that does not have a number
    cell = st.grid[y][x]
    if cell.state != st.NUMBER:
        return

    # If number is greater that last number,
    # the click is good
    if cell.value > last_value:
        last_value = cell.value
        cell.state = st.CLICK
        st.score += 1

    # Otherwise report the error and end the round
    else:
        cell.state = st.ERROR
        st.state = st.ST_NEXT

    # End the round when all numbers clicked
    number_count -= 1
    if number_count == 0:
        st.state = st.ST_NEXT
        if st.count < 10:
            st.count += 1


# ---------------------------------------------------------------------------
def clear_grid():
    """Clear the grid."""

    for y in range(st.GRID_HEIGHT):
        for x in range(st.GRID_WIDTH):
            st.grid[y][x].state = st.BLANK
