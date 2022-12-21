# ---------------------------------------------------------------------------
# Word Color
# Mike Christle 2022
# ---------------------------------------------------------------------------

import state as st

from pygame import K_LEFT, K_RIGHT
from random import randrange


# ---------------------------------------------------------------------------
def start_round():
    set_word_color()
    st.score = 0
    st.total = 0
    st.cycle += 1
    st.game_active = True


# ---------------------------------------------------------------------------
def set_word_color():
    st.left_word = randrange(4)
    st.left_color = randrange(4)
    st.right_word = randrange(4)
    st.right_color = randrange(4)
    st.word_color_match = st.left_word == st.right_color


# ---------------------------------------------------------------------------
def check(key):
    if (key == K_LEFT and not st.word_color_match) or \
       (key == K_RIGHT and st.word_color_match):
            st.score += 1

    st.total += 1
    set_word_color()
