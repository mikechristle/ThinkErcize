# ---------------------------------------------------------------------------
# Laser Path, State
# Mike Christle 2022
# ---------------------------------------------------------------------------

ST_IDLE = 1
ST_SHOW = 2
ST_WAIT = 3
ST_START = 4
ST_DONE = 5
state = ST_IDLE

EMPTY = 0
MIRROR1 = 1
MIRROR2 = 2
LASER_N = 3
LASER_E = 4
LASER_S = 5
LASER_W = 6

grid = [[EMPTY for _ in range(7)] for _ in range(7)]
score = 0
mirrors = 4
cycle = 0
click_x = 0
click_y = 0
