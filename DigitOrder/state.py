# ---------------------------------------------------------------------------
# Digit Order
# Mike Christle 2022
# ---------------------------------------------------------------------------

from dataclasses import make_dataclass

ST_IDLE = 1
ST_SHOW = 2
ST_WAIT = 3
ST_NEXT = 4
state = ST_IDLE

BLANK = 0
NUMBER = 1
CLICK = 2
ERROR = 3

GRID_WIDTH = 10
GRID_HEIGHT = 8
Cell = make_dataclass('Cell', ('value', 'state'))
grid = [[Cell(0, 0) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

score = 0
cycle = 0
count = 0
