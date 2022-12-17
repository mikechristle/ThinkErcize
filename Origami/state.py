# ---------------------------------------------------------------------------
# Origami
# Mike Christle 2022
# ---------------------------------------------------------------------------

ST_IDLE = 1
ST_WAIT = 2
ST_DONE = 3
state = ST_IDLE

FLIP_NONE = 0
FLIP_HORZ = 1
FLIP_VERT = 2
FLIP_BOTH = 3
FLIP_DIAG = 4
flip = FLIP_NONE

IMG_BLANK = 0
IMG_C = 1
IMG_D = 2
IMG_H = 3
IMG_S = 4
IMG_X = 5
grid = [[IMG_BLANK for _ in range(8)] for _ in range(8)]

cursor_x = 0
cursor_y = 0
cursor_img = 0

paper_w = 3
paper_h = 3

games = 0
score = 0
