# ---------------------------------------------------------------------------
# Maze Escape
# Construct 3D View
# Mike Christle 2023
# ---------------------------------------------------------------------------

import state as st

from math import sin, cos, pi
from paint import VIEW_WIDTH, VIEW_HEIGHT, walls

FOV = 0.7
ANGLE_FACTOR = pi / 4.0


# ---------------------------------------------------------------------------
def make_3d_view():
    """Construct a 3D view."""

    # Convert direction angle to radians
    angle = st.angle * ANGLE_FACTOR

    # Get direction vector
    dir_x = cos(angle)
    dir_y = -sin(angle)

    # Get view plane vector
    angle -= pi / 2.0
    plane_x = cos(angle) * FOV
    plane_y = -sin(angle) * FOV

    # Set position to middle of current cell
    pos_x = st.pos_x + 0.5
    pos_y = st.pos_y + 0.5

    # For each vertical line in image
    for x in range(VIEW_WIDTH):

        # Get the current ray vector
        camera_x = (2.0 * x / VIEW_WIDTH) - 1.0
        ray_x = dir_x + plane_x * camera_x
        ray_y = dir_y + plane_y * camera_x

        delta_x = 1e30 if ray_x == 0.0 else abs(1.0 / ray_x)
        delta_y = 1e30 if ray_y == 0.0 else abs(1.0 / ray_y)

        map_x = int(st.pos_x)
        map_y = int(st.pos_y)

        if ray_x < 0:
            step_x = -1
            side_x = (pos_x - map_x) * delta_x
        else:
            step_x = 1
            side_x = (map_x + 1.0 - pos_x) * delta_x

        if ray_y < 0:
            step_y = -1
            side_y = (pos_y - map_y) * delta_y
        else:
            step_y = 1
            side_y = (map_y + 1.0 - pos_y) * delta_y

        while True:
            if side_x < side_y:
                side_x += delta_x
                map_x += step_x
                side = 0
            else:
                side_y += delta_y
                map_y += step_y
                side = 1

            # Check if ray has hit a wall
            wall = st.grid[int(map_y)][int(map_x)]
            if wall > 0: break

        if side == 0:
            wall_dist = side_x - delta_x
        else:
            wall_dist = side_y - delta_y
        wall_height = int(VIEW_HEIGHT / wall_dist)

        if abs(dir_y) > abs(dir_x):
            side ^= 1
        wall = ((wall - 1) * 2) + side
        walls[x] = wall_height, wall
