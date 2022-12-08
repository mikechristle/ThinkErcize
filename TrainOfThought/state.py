# ---------------------------------------------------------------------------
# ThinkErcise, State
# Mike Christle 2022
# ---------------------------------------------------------------------------

GRID_WIDTH = 20
GRID_HEIGHT = 16

# grid keeps the state of each cell
grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Stores the location and state of each switch
switches = []

# stores the location and color of each active train
trains = []

# Number of barns in the route
difficulty_level = 4

# Total number of trains in a game
total_trains = 0

# Game is active
game_active = False

# Number of trains the found the right color of barn
game_score = 0

# Location of the tunnel
# starting location of all trains
tunnel_x = 0
tunnel_y = 0
