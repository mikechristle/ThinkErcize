# ---------------------------------------------------------------------------
# Best Route
# Mike Christle 2022
# ---------------------------------------------------------------------------

from cell import Cell

maze = [[Cell(x, y) for x in range(8)] for y in range(8)]
car = []

car_x = 0
car_y = 0
level = 3
grid_size = 5
house_count = 0
miles = 0
least_miles = 0

ST_INTRO = 0    # Show the instructions
ST_IDLE = 1     # Wait for player to select a level
ST_PLAY = 2     # Playing the game

state = ST_INTRO
