# ---------------------------------------------------------------------------
# Memory Patterns
# Current state of the game
# Mike Christle 2022
# ---------------------------------------------------------------------------

# Grid Width, Grid Height, Square Count
LEVELS = (
    (4, 4,  4), (5, 4,  5), (5, 5,  6),
    (6, 5,  7), (6, 5,  8), (6, 6,  9),
    (7, 6, 10), (7, 6, 11), (7, 7, 12),
)
level = 0

BLANK = 0
TILE = 1
CLICK = 2
ERROR = 3
grid = [[BLANK for _ in range(7)] for _ in range(7)]

ST_INTRO = 0
ST_SHOW = 1
ST_WAIT = 2
state = ST_INTRO

round = 0
