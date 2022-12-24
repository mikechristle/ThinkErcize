# ---------------------------------------------------------------------------
# Tile Match
# Mike Christle 2022
# ---------------------------------------------------------------------------

from dataclasses import make_dataclass

BLANK = 0
BORDER = 1
SQUARE = 2
DIAMOND = 3
CIRCLE = 4

Cell = make_dataclass('Cell', ('shape', 'color', 'orient', 'x0', 'y0'))

grid = [[Cell(0, 0, (x ^ y) & 1, 0, 0) for y in range(8)] for x in range(8)]

new_tile = Cell(0, 0, 0, 0, 0)
run_time = 0
delay_count = 0

ST_IDLE = 0
ST_START = 1
ST_PLAY = 2
state = ST_IDLE
