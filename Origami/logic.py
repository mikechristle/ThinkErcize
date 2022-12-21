# ---------------------------------------------------------------------------
# Origami
# Mike Christle 2022
# ---------------------------------------------------------------------------

import state as st
import pygame

from random import randrange, choice
from paint import paint_pattern, paint

CARDS = st.IMG_C, st.IMG_D, st.IMG_H, st.IMG_S
FLIPS = st.FLIP_VERT, st.FLIP_HORZ, st.FLIP_BOTH, st.FLIP_DIAG

pygame.mixer.init()
ding = pygame.mixer.Sound('Sounds/Ding.wav')
whoop = pygame.mixer.Sound('Sounds/Whoop.wav')
success = False


# ---------------------------------------------------------------------------
def check_click():
    """Check if the selected cell makes a valid fold."""

    # Only accept clicks on blank cells
    cell = st.grid[st.cursor_y][st.cursor_x]
    if cell != st.IMG_BLANK:
        return False

    # Set the cell to the cursor image
    st.grid[st.cursor_y][st.cursor_x] = st.cursor_img

    # Call the specific check routine
    match st.flip:
        case st.FLIP_HORZ: check_horz()
        case st.FLIP_VERT: check_vert()
        case st.FLIP_BOTH: check_both()
        case st.FLIP_DIAG: check_diag()

    # Clear the flip state, unless it is a diagonal flip
    # This is to make the paint look right
    if st.flip != st.FLIP_DIAG:
        st.flip = st.FLIP_NONE

    # Update the screen
    st.cursor_x = -1
    paint_pattern()
    paint()

    # Update the stats
    st.games += 1
    if success:
        st.score += 1
        ding.play()
    else:
        whoop.play()

    # Return true to indicate that the pattern was checked
    return True


# ---------------------------------------------------------------------------
def check_horz():
    """Check a horizontal flip pattern."""

    global success

    success = True
    max_x = (st.paper_w * 2) - 1
    for y in range(st.paper_h):
        for x in range(st.paper_w):
            cell0 = st.grid[y][x]
            cell1 = st.grid[y][max_x - x]
            if cell0 != st.IMG_BLANK and cell1 != st.IMG_BLANK:
                st.grid[y][x] = st.IMG_X
                success = False
            elif cell1 != st.IMG_BLANK:
                st.grid[y][x] = cell1
            st.grid[y][max_x - x] = st.IMG_BLANK


# ---------------------------------------------------------------------------
def check_vert():
    """Check a vertical flip pattern."""

    global success

    success = True
    max_y = (st.paper_h * 2) - 1
    for y in range(st.paper_h):
        for x in range(st.paper_w):
            cell0 = st.grid[y][x]
            cell1 = st.grid[max_y - y][x]
            if cell0 != st.IMG_BLANK and cell1 != st.IMG_BLANK:
                st.grid[y][x] = st.IMG_X
                success = False
            elif cell1 != st.IMG_BLANK:
                st.grid[y][x] = cell1
            st.grid[max_y - y][x] = st.IMG_BLANK


# ---------------------------------------------------------------------------
def check_both():
    """Check a both vertical and horizontal flip pattern."""

    global success

    success = True

    max_x = (st.paper_w * 2) - 1
    max_y = (st.paper_h * 2) - 1

    for y in range(st.paper_h):
        for x in range(st.paper_w):
            cell0 = st.grid[y][x]
            cell1 = st.grid[max_y - y][x]
            cell2 = st.grid[y][max_x - x]
            cell3 = st.grid[max_y - y][max_x - x]
            lst = cell0, cell1, cell2, cell3
            count = lst.count(st.IMG_BLANK)
            if count < 3:
                st.grid[y][x] = st.IMG_X
                success = False
            else:
                for cell in lst:
                    if cell != st.IMG_BLANK:
                        st.grid[y][x] = cell
                        break

            st.grid[max_y - y][x] = st.IMG_BLANK
            st.grid[y][max_x - x] = st.IMG_BLANK
            st.grid[max_y - y][max_x - x] = st.IMG_BLANK


# ---------------------------------------------------------------------------
def check_diag():
    """Check a diagonal flip pattern."""

    global success

    success = True
    for y in range(st.paper_h):
        for x in range(y + 1, st.paper_w + 1):
            if x == y:
                continue

            cell0 = st.grid[y][x]
            cell1 = st.grid[x][y]
            if cell0 != st.IMG_BLANK and cell1 != st.IMG_BLANK:
                st.grid[y][x] = st.IMG_X
                success = False
            elif cell1 != st.IMG_BLANK:
                st.grid[y][x] = cell1
            st.grid[x][y] = st.IMG_BLANK


# ---------------------------------------------------------------------------
def set_pattern():
    """Build a random pattern."""

    # Select a paper size and flip pattern
    st.paper_w = randrange(2, 5)
    st.paper_h = randrange(2, 5)
    st.flip = choice(FLIPS)

    st.cursor_img = choice(CARDS)
    st.cursor_x = -1

    # Clear the grid then fill with a pattern
    clear_grid()
    match st.flip:
        case st.FLIP_HORZ: flip_grid_horz()
        case st.FLIP_VERT: flip_grid_vert()
        case st.FLIP_BOTH: flip_grid_both()
        case st.FLIP_DIAG: flip_grid_diag()

    # Update the screen
    paint_pattern()


# ---------------------------------------------------------------------------
def flip_grid_horz():
    """Fill the grid for a horizontal flip."""

    fill_grid()
    max_x = (st.paper_w * 2) - 1
    count = st.paper_h * st.paper_w // 2
    while count > 0:
        x = randrange(st.paper_w)
        y = randrange(st.paper_h)
        c = st.grid[y][x]
        if c > st.IMG_BLANK:
            st.grid[y][x] = st.IMG_BLANK
            x = max_x - x
            st.grid[y][x] = c
            count -= 1


# ---------------------------------------------------------------------------
def flip_grid_vert():
    """Fill the grid for a vertical flip."""

    fill_grid()
    max_y = (st.paper_h * 2) - 1
    count = st.paper_h * st.paper_w // 2
    while count > 0:
        x = randrange(st.paper_w)
        y = randrange(st.paper_h)
        c = st.grid[y][x]
        if c > st.IMG_BLANK:
            st.grid[y][x] = st.IMG_BLANK
            y = max_y - y
            st.grid[y][x] = c
            count -= 1


# ---------------------------------------------------------------------------
def flip_grid_both():
    """Fill the grid for a vertical and horizontal flip."""

    fill_grid()

    # Flip vertically
    max_y = (st.paper_h * 2) - 1
    count = st.paper_h * st.paper_w // 2
    while count > 0:
        x = randrange(st.paper_w)
        y = randrange(st.paper_h)
        c = st.grid[y][x]
        if c > st.IMG_BLANK:
            st.grid[y][x] = st.IMG_BLANK
            y = max_y - y
            st.grid[y][x] = c
            count -= 1

    # Flip horizontally
    max_x = (st.paper_w * 2) - 1
    count = st.paper_h * st.paper_w // 2
    while count > 0:
        x = randrange(st.paper_w)
        y = randrange(st.paper_h * 2)
        c = st.grid[y][x]
        if c > st.IMG_BLANK:
            st.grid[y][x] = st.IMG_BLANK
            x = max_x - x
            st.grid[y][x] = c
            count -= 1


# ---------------------------------------------------------------------------
def flip_grid_diag():
    """Fill the grid for a diagonal flip."""

    # Fill the grid
    lst = []
    st.paper_h = st.paper_w
    for y in range(st.paper_h):
        for x in range(y + 1, st.paper_w + 1):
            st.grid[y][x] = choice(CARDS)
            lst.append((x, y))

    # Remove one card
    x, y = choice(lst)
    st.grid[y][x] = st.IMG_BLANK
    lst.remove((x, y))

    # Flip
    count = len(lst) // 2
    while count > 0:
        x, y = choice(lst)
        c = st.grid[y][x]
        if c > st.IMG_BLANK:
            st.grid[y][x] = st.IMG_BLANK
            st.grid[x][y] = c
            count -= 1


# ---------------------------------------------------------------------------
def fill_grid():
    """Fill the grid with random cards, then delete one."""

    for y in range(st.paper_h):
        for x in range(st.paper_w):
            st.grid[y][x] = choice(CARDS)

    x = randrange(st.paper_w)
    y = randrange(st.paper_h)
    st.grid[y][x] = st.IMG_BLANK


# ---------------------------------------------------------------------------
def clear_grid():
    """Clear the grid."""

    for y in range(8):
        for x in range(8):
            st.grid[y][x] = st.IMG_BLANK
