# ---------------------------------------------------------------------------
# Best Route
# Mike Christle 2022
# ---------------------------------------------------------------------------

from cell import Cell

maze = [[Cell(x, y) for x in range(8)] for y in range(8)]
car = []

car_x = 0
car_y = 0
level = 4
house_count = 0
miles = 0

ST_INTRO = 0    # Show the instructions
ST_IDLE = 1     #
ST_PLAY = 2     # Playing the game
ST_WAIT = 3     # Wait for player to select a level
state = ST_INTRO
