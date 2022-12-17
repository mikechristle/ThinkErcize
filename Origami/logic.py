# ---------------------------------------------------------------------------
# Origami
# Mike Christle 2022
# ---------------------------------------------------------------------------

import random
import state
import pygame

from paint import paint_pattern, paint

CARDS = state.IMG_C, state.IMG_D, state.IMG_H, state.IMG_S
FLIPS = state.FLIP_VERT, state.FLIP_HORZ, state.FLIP_BOTH, state.FLIP_DIAG

pygame.mixer.init()
ding = pygame.mixer.Sound('Sounds/Ding.wav')
whoop = pygame.mixer.Sound('Sounds/Whoop.wav')
success = False


# ---------------------------------------------------------------------------
def check_click():
    """Check if the selected cell makes a valid fold."""

    # Only accept clicks on blank cells
    cell = state.grid[state.cursor_y][state.cursor_x]
    if cell != state.IMG_BLANK:
        return False

    # Set the cell to the cursor image
    state.grid[state.cursor_y][state.cursor_x] = state.cursor_img

    # Call the specific check routine
    match state.flip:
        case state.FLIP_HORZ: check_horz()
        case state.FLIP_VERT: check_vert()
        case state.FLIP_BOTH: check_both()
        case state.FLIP_DIAG: check_diag()

    # Clear the flip state, unless it is a diagonal flip
    # This is to make the paint look right
    if state.flip != state.FLIP_DIAG:
        state.flip = state.FLIP_NONE

    # Update the screen
    state.cursor_x = -1
    paint_pattern()
    paint()

    # Update the stats
    state.games += 1
    if success:
        state.score += 1
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
    max_x = (state.paper_w * 2) - 1
    for y in range(state.paper_h):
        for x in range(state.paper_w):
            cell0 = state.grid[y][x]
            cell1 = state.grid[y][max_x - x]
            if cell0 != state.IMG_BLANK and cell1 != state.IMG_BLANK:
                state.grid[y][x] = state.IMG_X
                success = False
            elif cell1 != state.IMG_BLANK:
                state.grid[y][x] = cell1
            state.grid[y][max_x - x] = state.IMG_BLANK


# ---------------------------------------------------------------------------
def check_vert():
    """Check a vertical flip pattern."""

    global success

    success = True
    max_y = (state.paper_h * 2) - 1
    for y in range(state.paper_h):
        for x in range(state.paper_w):
            cell0 = state.grid[y][x]
            cell1 = state.grid[max_y - y][x]
            if cell0 != state.IMG_BLANK and cell1 != state.IMG_BLANK:
                state.grid[y][x] = state.IMG_X
                success = False
            elif cell1 != state.IMG_BLANK:
                state.grid[y][x] = cell1
            state.grid[max_y - y][x] = state.IMG_BLANK


# ---------------------------------------------------------------------------
def check_both():
    """Check a both vertical and horizontal flip pattern."""

    global success

    success = True

    max_x = (state.paper_w * 2) - 1
    max_y = (state.paper_h * 2) - 1

    for y in range(state.paper_h):
        for x in range(state.paper_w):
            cell0 = state.grid[y][x]
            cell1 = state.grid[max_y - y][x]
            cell2 = state.grid[y][max_x - x]
            cell3 = state.grid[max_y - y][max_x - x]
            lst = cell0, cell1, cell2, cell3
            count = lst.count(state.IMG_BLANK)
            if count < 3:
                state.grid[y][x] = state.IMG_X
                success = False
            else:
                for cell in lst:
                    if cell != state.IMG_BLANK:
                        state.grid[y][x] = cell
                        break

            state.grid[max_y - y][x] = state.IMG_BLANK
            state.grid[y][max_x - x] = state.IMG_BLANK
            state.grid[max_y - y][max_x - x] = state.IMG_BLANK


# ---------------------------------------------------------------------------
def check_diag():
    """Check a diagonal flip pattern."""

    global success

    success = True
    for y in range(state.paper_h):
        for x in range(y + 1, state.paper_w + 1):
            if x == y:
                continue

            cell0 = state.grid[y][x]
            cell1 = state.grid[x][y]
            if cell0 != state.IMG_BLANK and cell1 != state.IMG_BLANK:
                state.grid[y][x] = state.IMG_X
                success = False
            elif cell1 != state.IMG_BLANK:
                state.grid[y][x] = cell1
            state.grid[x][y] = state.IMG_BLANK


# ---------------------------------------------------------------------------
def set_pattern():
    """Build a random pattern."""

    # Select a paper size and flip pattern
    state.paper_w = random.randrange(2, 5)
    state.paper_h = random.randrange(2, 5)
    state.flip = random.choice(FLIPS)

    state.cursor_img = random.choice(CARDS)
    state.cursor_x = -1

    # Clear the grid then fill with a pattern
    clear_grid()
    match state.flip:
        case state.FLIP_HORZ: flip_grid_horz()
        case state.FLIP_VERT: flip_grid_vert()
        case state.FLIP_BOTH: flip_grid_both()
        case state.FLIP_DIAG: flip_grid_diag()

    # Update the screen
    paint_pattern()


# ---------------------------------------------------------------------------
def flip_grid_horz():
    """Fill the grid for a horizontal flip."""

    fill_grid()
    max_x = (state.paper_w * 2) - 1
    count = state.paper_h * state.paper_w // 2
    while count > 0:
        x = random.randrange(state.paper_w)
        y = random.randrange(state.paper_h)
        c = state.grid[y][x]
        if c > state.IMG_BLANK:
            state.grid[y][x] = state.IMG_BLANK
            x = max_x - x
            state.grid[y][x] = c
            count -= 1


# ---------------------------------------------------------------------------
def flip_grid_vert():
    """Fill the grid for a vertical flip."""

    fill_grid()
    max_y = (state.paper_h * 2) - 1
    count = state.paper_h * state.paper_w // 2
    while count > 0:
        x = random.randrange(state.paper_w)
        y = random.randrange(state.paper_h)
        c = state.grid[y][x]
        if c > state.IMG_BLANK:
            state.grid[y][x] = state.IMG_BLANK
            y = max_y - y
            state.grid[y][x] = c
            count -= 1


# ---------------------------------------------------------------------------
def flip_grid_both():
    """Fill the grid for a vertical and horizontal flip."""

    fill_grid()

    # Flip vertically
    max_y = (state.paper_h * 2) - 1
    count = state.paper_h * state.paper_w // 2
    while count > 0:
        x = random.randrange(state.paper_w)
        y = random.randrange(state.paper_h)
        c = state.grid[y][x]
        if c > state.IMG_BLANK:
            state.grid[y][x] = state.IMG_BLANK
            y = max_y - y
            state.grid[y][x] = c
            count -= 1

    # Flip horizontally
    max_x = (state.paper_w * 2) - 1
    count = state.paper_h * state.paper_w // 2
    while count > 0:
        x = random.randrange(state.paper_w)
        y = random.randrange(state.paper_h * 2)
        c = state.grid[y][x]
        if c > state.IMG_BLANK:
            state.grid[y][x] = state.IMG_BLANK
            x = max_x - x
            state.grid[y][x] = c
            count -= 1


# ---------------------------------------------------------------------------
def flip_grid_diag():
    """Fill the grid for a diagonal flip."""

    # Fill the grid
    lst = []
    state.paper_h = state.paper_w
    for y in range(state.paper_h):
        for x in range(y + 1, state.paper_w + 1):
            state.grid[y][x] = random.choice(CARDS)
            lst.append((x, y))

    # Remove one card
    x, y = random.choice(lst)
    state.grid[y][x] = state.IMG_BLANK
    lst.remove((x, y))

    # Flip
    count = len(lst) // 2
    while count > 0:
        x, y = random.choice(lst)
        c = state.grid[y][x]
        if c > state.IMG_BLANK:
            state.grid[y][x] = state.IMG_BLANK
            state.grid[x][y] = c
            count -= 1


# ---------------------------------------------------------------------------
def fill_grid():
    """Fill the grid with random cards, then delete one."""

    for y in range(state.paper_h):
        for x in range(state.paper_w):
            state.grid[y][x] = random.choice(CARDS)

    x = random.randrange(state.paper_w)
    y = random.randrange(state.paper_h)
    state.grid[y][x] = state.IMG_BLANK


# ---------------------------------------------------------------------------
def clear_grid():
    """Clear the grid."""

    for y in range(8):
        for x in range(8):
            state.grid[y][x] = state.IMG_BLANK
