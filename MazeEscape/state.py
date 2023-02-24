# ---------------------------------------------------------------------------
# Maze Escape
# Mike Christle 2023
# ---------------------------------------------------------------------------

from cell import Cell
from numpy import zeros

MAZE_SIZE = 8

maze = [[Cell(x, y) for x in range(MAZE_SIZE)] for y in range(MAZE_SIZE)]

GRID_CELL = 4
GRID_SIZE = (MAZE_SIZE * GRID_CELL) + 1
grid = zeros((GRID_SIZE, GRID_SIZE), dtype = int)

game_active = False

pos_x = GRID_CELL // 2
pos_y = GRID_CELL // 2
angle = 0
run_time = 0
