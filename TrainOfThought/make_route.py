# ---------------------------------------------------------------------------
# Train of Thought
# Fill the state variables to describe a route.
# Mike Christle 2022
# ---------------------------------------------------------------------------
# T = Tunnel
# S = Switch
# B = Barn
# 1 = Turn Right to Down
# 2 = Turn Down to Left
# 3 = Turn Left to Up
# 4 = Turn Up to Right
# 5 = Turn Right to Up
# 6 = Turn Up to Left
# 7 = Turn Left to Down
# 8 = Turn Down to Right
# > = Right Horizontal Track
# < = Left Horizontal Track
# ^ = Up Vertical Track
# v = Down Vertical Track
# ---------------------------------------------------------------------------

import state as st

from random import shuffle, choice
from routes import get_route
from enum_types import FuncT, DirT, FlipT, TrackT

GRID_WIDTH_MAX = st.GRID_WIDTH - 1
GRID_HEIGHT_MAX = st.GRID_HEIGHT - 1

barn_colors = []
barn_color = 0
text = []


# ---------------------------------------------------------------------------
def make_route():
    """Initialize a new route."""

    global text, barn_colors, barn_color

    # Clear the previous route
    st.switches.clear()
    for y in range(st.GRID_HEIGHT):
        for x in range(st.GRID_WIDTH):
            st.grid[y][x] = None

    # Setup barn colors based on difficulty level.
    barn_colors = [n for n in range(st.difficulty_level)]
    shuffle(barn_colors)
    barn_color = 0

    # To increase variety the route can be flipped vertically, 
    # horizontally, or both.
    flip = choice((FlipT.NONE, FlipT.VERT, FlipT.HORZ, FlipT.BOTH))

    # Get a route in text form.
    text = get_route()

    # Process the route
    process_grid(flip)


# ---------------------------------------------------------------------------
def process_grid(flip):
    """Fill the grid data structure with a new route."""

    # For each character in the text route,
    # update the corresponding location in the grid.
    for y in range(st.GRID_HEIGHT):
        for x in range(st.GRID_WIDTH):
            char = text[y][x]
            match char:
                case '>':
                    st.grid[y][x] = track(char, flip)
                case '<':
                    st.grid[y][x] = track(char, flip)
                case '^':
                    st.grid[y][x] = track(char, flip)
                case 'V':
                    st.grid[y][x] = track(char, flip)
                case '1':
                    st.grid[y][x] = turn(char, flip)
                case '2':
                    st.grid[y][x] = turn(char, flip)
                case '3':
                    st.grid[y][x] = turn(char, flip)
                case '4':
                    st.grid[y][x] = turn(char, flip)
                case '5':
                    st.grid[y][x] = turn(char, flip)
                case '6':
                    st.grid[y][x] = turn(char, flip)
                case '7':
                    st.grid[y][x] = turn(char, flip)
                case '8':
                    st.grid[y][x] = turn(char, flip)
                case 'T':
                    st.grid[y][x] = tunnel(x, y, flip)
                case 'B':
                    st.grid[y][x] = barn(x, y, flip)
                case 'S':
                    st.grid[y][x] = switch(x, y, flip)
                case '.' | '\n':
                    pass
                case _:
                    raise Exception(f'INVALID TEXT FILE {x} {y} ({char})')

    # For a horizontal flip, reverse the elements of each row
    if flip == FlipT.HORZ or flip == FlipT.BOTH:
        for row in st.grid:
            row.reverse()

    # For a vertical flip, reverse the rows
    if flip == FlipT.VERT or flip == FlipT.BOTH:
        st.grid.reverse()


# ---------------------------------------------------------------------------
def turn(char, flip):
    """Process a turn in the track."""

    # direction indicates how a train moves when leaving this cell.
    # img indicates which bitmap image to paint for this cell.
    match char:
        case '1': direction, img = DirT.DOWN,  TrackT.DR
        case '2': direction, img = DirT.LEFT,  TrackT.UL
        case '3': direction, img = DirT.UP,    TrackT.UR
        case '4': direction, img = DirT.RIGHT, TrackT.DL
        case '5': direction, img = DirT.UP,    TrackT.UL
        case '6': direction, img = DirT.LEFT,  TrackT.DR
        case '7': direction, img = DirT.DOWN,  TrackT.DL
        case '8': direction, img = DirT.RIGHT, TrackT.UR
        case _:
            raise Exception("Invalid route text, {char}.")

    # Update the direction base on flip
    direction = flip_dir(direction, flip)

    # Update the image based on flip
    match [img, flip]:
        case [TrackT.DR, FlipT.HORZ]: img = TrackT.DL
        case [TrackT.DL, FlipT.HORZ]: img = TrackT.DR
        case [TrackT.UR, FlipT.HORZ]: img = TrackT.UL
        case [TrackT.UL, FlipT.HORZ]: img = TrackT.UR
        case [TrackT.DR, FlipT.VERT]: img = TrackT.UL
        case [TrackT.DL, FlipT.VERT]: img = TrackT.UR
        case [TrackT.UR, FlipT.VERT]: img = TrackT.DL
        case [TrackT.UL, FlipT.VERT]: img = TrackT.DR
        case [TrackT.DR, FlipT.BOTH]: img = TrackT.UR
        case [TrackT.DL, FlipT.BOTH]: img = TrackT.UL
        case [TrackT.UR, FlipT.BOTH]: img = TrackT.DR
        case [TrackT.UL, FlipT.BOTH]: img = TrackT.DL

    return FuncT.TURN, direction, img


# ---------------------------------------------------------------------------
def track(char, flip):
    """Process a straight track segment."""

    # direction indicates how a train moves when leaving this cell.
    match char:
        case '>': direction = DirT.RIGHT
        case '<': direction = DirT.LEFT
        case '^': direction = DirT.UP
        case 'V': direction = DirT.DOWN
        case _: raise Exception("Invalid route text, {char}.")

    # Update the direction base on flip
    direction = flip_dir(direction, flip)
    return FuncT.TRACK, direction


# ---------------------------------------------------------------------------
def switch(x, y, flip):
    """Process a switch."""

    #  Get the contents of the four neighboring cells.
    t = None if y == 0 else text[y - 1][x]
    b = None if y == GRID_HEIGHT_MAX else text[y + 1][x]
    l = None if x == 0 else text[y][x - 1]
    r = None if x == GRID_WIDTH_MAX else text[y][x + 1]

    # dir0 is the direction of travel if the switch state is False.
    # dir1 is the direction of travel if the switch state is True.
    dir0 = dir1 = None

    # dir0 is determined by which neighbor points into this cell.
    # When the switch state is False, a train travels straight
    # through the switch. When the switch state is True the train
    # turns through the switch. So dir1 is determined by which
    # neighbor has a perpendicular route out of the cell.
    match [t, b, l, r]:
        case ['^' | '4' | '6', _, '>' | '4' | '8', _]:
            dir0, dir1 = DirT.RIGHT, DirT.UP
        case [_, 'V' | '2' | '8', '>' | '4' | '8', _]:
            dir0, dir1 = DirT.RIGHT, DirT.DOWN
        case ['^' | '4' | '6', _, _, '<' | '2' | '6']:
            dir0, dir1 = DirT.LEFT, DirT.UP
        case [_, 'V' | '2' | '8', _, '<' | '2' | '6']:
            dir0, dir1 = DirT.LEFT, DirT.DOWN
        case [_, '^' | '3' | '5', _, '>' | '1' | '5']:
            dir0, dir1 = DirT.UP, DirT.RIGHT
        case [_, '^' | '3' | '5', '<' | '3' | '7', _]:
            dir0, dir1 = DirT.UP, DirT.LEFT
        case ['V' | '1' | '7', _, _, '>' | '1' | '5']:
            dir0, dir1 = DirT.DOWN, DirT.RIGHT
        case ['V' | '1' | '7', _, '<' | '3' | '7', _]:
            dir0, dir1 = DirT.DOWN, DirT.LEFT
        case [_, _, _, _]:
            raise Exception(f'Invalid route text. {x}, {y}')

    # Flip the state of the switch.
    dir0 = flip_dir(dir0, flip)
    dir1 = flip_dir(dir1, flip)
    x, y = flip_xy(x, y, flip)

    # Save the state of the switch.
    st.switches.append([x, y, dir0, dir1, False])
    return FuncT.SWITCH, len(st.switches) - 1


# ---------------------------------------------------------------------------
def barn(x, y, flip):
    """Process a barn."""

    global barn_color

    # Get the next random barn color.
    color = barn_colors[barn_color]
    barn_color += 1

    #  Get the contents of the four neighboring cells.
    t = None if y == 0 else text[y - 1][x]
    b = None if y == GRID_HEIGHT_MAX else text[y + 1][x]
    l = None if x == 0 else text[y][x - 1]
    r = None if x == GRID_WIDTH_MAX else text[y][x + 1]

    # direction indicates how the train enters the barn.
    direction = None
    match [t, b, l, r]:
        case [_, '^' | '3' | '5', _, _]: direction = DirT.UP
        case [_, _, '>' | '4' | '8', _]: direction = DirT.RIGHT
        case ['V' | '1' | '7', _, _, _]: direction = DirT.DOWN
        case [_, _, _, '<' | '2' | '6']: direction = DirT.LEFT
        case [_, _, _, _]:
            raise Exception("Invalid route text. {x}, {y}")

    # Flip the direction.
    direction = flip_dir(direction, flip)

    return FuncT.BARN, direction, color


# ---------------------------------------------------------------------------
def tunnel(x, y, flip):
    """Process a tunnel."""

    #  Get the contents of the four neighboring cells.
    t = None if y == 0 else text[y - 1][x]
    b = None if y == GRID_HEIGHT_MAX else text[y + 1][x]
    l = None if x == 0 else text[y][x - 1]
    r = None if x == GRID_WIDTH_MAX else text[y][x + 1]

    # direction indicates how a train will leave the tunnel.
    direction = None
    match [t, b, l, r]:
        case [_, 'V' | '2' | '8', _, _]: direction = DirT.DOWN
        case [_, _, '<' | '3' | '7', _]: direction = DirT.LEFT
        case ['^' | '4' | '6', _, _, _]: direction = DirT.UP
        case [_, _, _, '>' | '1' | '5']: direction = DirT.RIGHT
        case [_, _, _, _]:
            raise Exception("Invalid route text. {x}, {y}")

    # Flip the direction.
    direction = flip_dir(direction, flip)

    # Save the location of the tunnel so trains can be added.
    st.tunnel_x, st.tunnel_y = flip_xy(x, y, flip)

    return FuncT.TUNNEL, direction


# ---------------------------------------------------------------------------
def flip_xy(x, y, flip):
    """Flip a pair of x, y coordinates."""

    match flip:
        case FlipT.HORZ:
            x = GRID_WIDTH_MAX - x
        case FlipT.VERT:
            y = GRID_HEIGHT_MAX - y
        case FlipT.BOTH:
            x = GRID_WIDTH_MAX - x
            y = GRID_HEIGHT_MAX - y

    return x, y


# ---------------------------------------------------------------------------
def flip_dir(direction, flip):
    """Flip the direction."""

    match [direction, flip]:
        case [DirT.RIGHT, FlipT.HORZ | FlipT.BOTH]:
            direction = DirT.LEFT
        case [DirT.LEFT, FlipT.HORZ | FlipT.BOTH]:
            direction = DirT.RIGHT
        case [DirT.UP, FlipT.VERT | FlipT.BOTH]:
            direction = DirT.DOWN
        case [DirT.DOWN, FlipT.VERT | FlipT.BOTH]:
            direction = DirT.UP

    return direction
