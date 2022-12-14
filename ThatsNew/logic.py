# ---------------------------------------------------------------------------
# That's New
# Game logic.
# Mike Christle 2022
# ---------------------------------------------------------------------------

import state as st
from random import randrange, shuffle

clicked_images = set()
remaining_images = []


# ---------------------------------------------------------------------------
def init_game():
    """Setup for a new game."""

    global remaining_images

    clicked_images.clear()
    remaining_images = [x for x in range(1, 53)]
    update_grid()
    st.game_active = True


# ---------------------------------------------------------------------------
def update_grid():
    """
    Place the clicked images and three new images
    at random locations on the grid.
    """

    # Clear the grid
    for y in range(6):
        for x in range(8):
            st.grid[y][x] = 0, st.BLANK

    # Setup random grid indices
    grid_idx = [x for x in range(48)]
    shuffle(grid_idx)

    # Add all clicked images
    for cell in clicked_images:
        idx = grid_idx.pop(0)
        st.grid[idx // 8][idx % 8] = cell, st.CLICK

    # Select three more images
    temp = set()
    while len(temp) < 3:
        n = randrange(len(remaining_images))
        temp.add(remaining_images[n])

    # Add up to three images, unless the grid is full
    for cell in temp:
        if len(grid_idx) > 0:
            idx = grid_idx.pop(0)
            st.grid[idx // 8][idx % 8] = cell, st.NEW


# ---------------------------------------------------------------------------
def click(x, y):
    """Process clicks."""

    # Ignore clicks on the status bar
    if y > 5:
        return

    # Ignore clicks on blank squares
    idx, status = st.grid[y][x]
    if status == st.BLANK:
        return

    # If clicked on a new image
    if status == st.NEW:

        # Move image to the clicked set
        remaining_images.remove(idx)
        clicked_images.add(idx)

        # If clicked image set is full, end the game
        if len(clicked_images) >= 48:
            st.grid[y][x] = idx, st.CLICK
            st.game_active = False

        # Else, add more images
        else:
            update_grid()

    # If image has already been clicked,
    # mark as an error and end game
    elif status == st.CLICK:
        st.grid[y][x] = idx, st.ERROR
        st.game_active = False
