# ---------------------------------------------------------------------------
# That's New
# The current state of the game.
# Mike Christle 2022
# ---------------------------------------------------------------------------

BLANK = 0
NEW = 1
CLICK = 2
ERROR = 3

grid = [[(0, BLANK) for _ in range(8)] for _ in range(6)]
game_active = False
