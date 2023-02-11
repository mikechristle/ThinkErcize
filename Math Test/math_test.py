# ---------------------------------------------------------------------------
# Math Test
# Mike Christle 2023
# ---------------------------------------------------------------------------

import pygame as py
import state as st

from sys import exit
from random import randrange
from time import time
from paint import paint, paint_intro

result_left = 0
result_right = 0
cycle = 0


# ---------------------------------------------------------------------------
def main():
    """Main routine."""

    global cycle

    # Display the intro screen
    paint_intro()

    while True:

        # Get all pygame events
        for event in py.event.get():
            match [event.type, st.game_active]:

                # Exit if window is closed
                case [py.QUIT, _]:
                    exit()

                # Start a new game when space bar is pressed
                case [py.KEYDOWN, False]:
                    if event.key == py.K_SPACE:
                        cycle = 20
                        st.score = 0
                        st.game_active = True
                        st.time = time()
                        setup_round()
                        paint()

                # Check results for each pair of expressions
                case [py.KEYDOWN, True]:
                    match event.key:
                        case py.K_UP | py.K_DOWN:
                            if result_left == result_right:
                                st.score += 1
                        case py.K_RIGHT:
                            if result_left < result_right:
                                st.score += 1
                        case py.K_LEFT:
                            if result_left > result_right:
                                st.score += 1
                        case _:
                            continue

                    # Check for end of game
                    cycle -= 1
                    if cycle == 0:
                        st.game_active = False
                        st.time = time() - st.time
                    else:
                        setup_round()
                    paint()


# ---------------------------------------------------------------------------
def setup_round():
    """Setup two expressions for the next round."""

    global result_left, result_right

    st.eq_left, result_left = make_expression()
    st.eq_right, result_right = make_expression()


# ---------------------------------------------------------------------------
def make_expression():
    """Construct a random expression."""

    v1 = randrange(1, 10)
    v2 = randrange(1, 10)

    op1, result = get_op(v1, v2)
    if cycle > 5:
        return f'{v1} {op1} {v2}', result

    v3 = randrange(1, 10)
    op2, result = get_op(result, v3)
    return f'({v1} {op1} {v2}) {op2} {v3}', result


# ---------------------------------------------------------------------------
def get_op(v1, v2):
    """Pick a random operation."""

    match randrange(4):
        case 0:
            return '+', v1 + v2
        case 1:
            return '-', v1 - v2
        case 2:
            return '*', v1 * v2
        case 3:
            return '/', v1 / v2


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()

