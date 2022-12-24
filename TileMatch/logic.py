# ---------------------------------------------------------------------------
# Tile Match
# Mike Christle 2022
# ---------------------------------------------------------------------------

import state as st

from random import randrange

VERT = 0
HORZ = 1

# Tracks number of active tiles to determine end of game
tile_count = 0


# ---------------------------------------------------------------------------
def clear_grid():
    """Clear all cells in the grid."""

    for y in range(8):
        for x in range(8):
            st.grid[y][x].shape = st.BLANK


# ---------------------------------------------------------------------------
def pick_new_tile():
    """
    Randomly pick a new tile. It is only valid if it allows at
    least one other tile to be removed.
    """

    valid_new_tile = False

    while not valid_new_tile:

        # Randomly pick a new tile
        st.new_tile.shape = randrange(2, 5)
        st.new_tile.color = randrange(3)
        st.new_tile.orient = randrange(2)

        # For each cell in the grid
        for y in range(8):
            for x in range(8):
                cell = st.grid[y][x]

                # Ignore color tiles
                if cell.shape > st.BORDER:
                    continue

                # Clear all non-color tiles
                cell.shape = st.BLANK

                # Ignore if not oriented the same as new tile
                if cell.orient != st.new_tile.orient:
                    continue

                # Ignore if there are no neighbors
                neighbors = get_neighbors(x, y)
                if len(neighbors) == 0:
                    continue

                # Count how many neighbors can be removed
                cell.shape = st.BORDER
                count = 0
                if st.new_tile.orient == HORZ:
                    for other in neighbors:
                        if other.shape == st.new_tile.shape:
                            count += 1
                else:
                    for other in neighbors:
                        if other.color == st.new_tile.color:
                            count += 1

                # If all neighbors can be removed,
                # this is a valid new tile
                if count == len(neighbors):
                    valid_new_tile = True


# ---------------------------------------------------------------------------
def click(x, y):
    """Process a click."""

    global tile_count

    # Ignore if click not on the tiles
    if x < 0 or x > 7 or y < 0 or y > 7:
        return False

    # Ignore if tile is not a border tile
    if st.grid[y][x].shape != st.BORDER:
        return False

    valid_match = True
    lst = get_neighbors(x, y)

    # Check that all neighbors are correct color
    if st.new_tile.orient == VERT:
        for other in lst:
            if st.new_tile.color != other.color:
                valid_match = False

    # Check that all neighbors are correct shape
    else: # st.new_tile.orient == HORZ
        for other in lst:
            if st.new_tile.shape != other.shape:
                valid_match = False

    # If a valid match, remove neighbor tiles
    if valid_match:
        for other in lst:
            other.shape = st.BLANK
            tile_count -= 1

    # Else add new tile to grid
    else:
        st.grid[y][x].shape = st.new_tile.shape
        st.grid[y][x].color = st.new_tile.color
        tile_count += 1

    # If all tiles are removed, the the game
    if tile_count == 0:
        st.state = st.ST_IDLE

    # Return true to indicate a valid click
    return True


# ---------------------------------------------------------------------------
def get_neighbors(x, y):
    """Get a list of all neighbors that have color."""

    lst = []
    if y > 0:
        cell = st.grid[y - 1][x]
        if cell.shape > st.BORDER:
            lst.append(cell)
    if y < 7:
        cell = st.grid[y + 1][x]
        if cell.shape > st.BORDER:
            lst.append(cell)
    if x > 0:
        cell = st.grid[y][x - 1]
        if cell.shape > st.BORDER:
            lst.append(cell)
    if x < 7:
        cell = st.grid[y][x + 1]
        if cell.shape > st.BORDER:
            lst.append(cell)
    return lst


# ---------------------------------------------------------------------------
def start_game():

    """Setup for a new game."""
    global tile_count

    tile_count = 36

    # Fill the edges with blanks
    for y in range(8):
        st.grid[y][0].shape = st.BLANK
        st.grid[y][7].shape = st.BLANK

    for x in range(8):
        st.grid[0][x].shape = st.BLANK
        st.grid[7][x].shape = st.BLANK

    # Fill the rest with random tiles
    for y in range(1, 7):
        for x in range(1, 7):
            st.grid[y][x].shape = randrange(2, 5)
            st.grid[y][x].color = randrange(3)
