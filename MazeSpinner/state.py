# ---------------------------------------------------------------------------
# Maze Spinner
# The current state of the game.
# Mike Christle 2022
# ---------------------------------------------------------------------------

from cell import Cell

MAZE_SIZE = 12

maze = [[Cell(x, y) for x in range(MAZE_SIZE)] for y in range(MAZE_SIZE)]
game_active = False

ball_x = 0
ball_y = 0
rotation_angle = 0.0
elapsed_time = 0.0
