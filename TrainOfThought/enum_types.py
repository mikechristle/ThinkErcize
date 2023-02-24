# ---------------------------------------------------------------------------
# Train of Thought
# Mike Christle 2022
# ---------------------------------------------------------------------------
from enum import Enum


class TrackT(Enum):
    """Indicates which image to paint for a track segment."""
    HZ = 0
    VT = 1
    DL = 2
    DR = 3
    UL = 4
    UR = 5


class DirT(Enum):
    """Indicates the direction of travel."""
    UP    = 0
    RIGHT = 1
    DOWN  = 2
    LEFT  = 3


class FuncT(Enum):
    """Indicates what each cell in the grid contains."""
    NONE   = 0
    TRACK  = 1
    TURN   = 2
    SWITCH = 3
    BARN   = 4
    TUNNEL = 5


class FlipT(Enum):
    """Indicates how to flip a route."""
    NONE = 0
    VERT = 1
    HORZ = 2
    BOTH = 3
