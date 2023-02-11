# ---------------------------------------------------------------------------
# Who Am I
# Mike Christle 2022
# ---------------------------------------------------------------------------

import state as st

from images import FACES
from random import shuffle
from paint import paint, get_name_idx, paint_status


FEMALE_NAMES = (
    'Olivia', 'Emma', 'Amelia', 'Ava', 'Sophia', 'Isabella', 'Luna',
    'Mia', 'Charlotte', 'Evelyn', 'Harper', 'Scarlett', 'Nova', 'Aurora',
    'Ella', 'Mila', 'Aria', 'Ellie', 'Gianna', 'Sofia', 'Violet', 'Layla',
    'Willow', 'Lily', 'Hazel', 'Camila', 'Avery', 'Chloe', 'Elena',
    'Paisley', 'Eliana', 'Penelope', 'Eleanor', 'Ivy', 'Elizabeth',
    'Riley', 'Isla', 'Abigail', 'Nora', 'Stella', 'Grace', 'Zoey', 'Emily',
    'Emilia', 'Leilani', 'Everly', 'Kinsley', 'Athena', 'Delilah', 'Naomi'
)

MALE_NAMES = (
    'Liam', 'Noah', 'Oliver', 'Elijah', 'Mateo', 'Lucas', 'Levi', 'Asher',
    'James', 'Leo', 'Grayson', 'Ezra', 'Luca', 'Ethan', 'Aiden', 'Wyatt',
    'Sebastian', 'Benjamin', 'Mason', 'Henry', 'Hudson', 'Jack', 'Jackson',
    'Owen', 'Daniel', 'Alexander', 'Maverick', 'Kai', 'Gabriel', 'Carter',
    'William', 'Logan', 'Michael', 'Samuel', 'Muhammad', 'Waylon',
    'Ezekiel', 'Jayden', 'Luke', 'Lincoln', 'Theo', 'Jacob', 'Josiah',
    'David', 'Jaxon', 'Elias', 'Julian', 'Theodore', 'Isaiah', 'Matthew'
)

img_count = 0
round_score = 0
img_indices = [x for x in range(len(FACES))]
name_indices = [x for x in range(len(FEMALE_NAMES))]


# ---------------------------------------------------------------------------
def start_game():
    st.score = 0
    st.cycle = 0


# ---------------------------------------------------------------------------
def start_round():
    global img_count, round_score

    round_score = 0
    img_count = st.level
    shuffle(img_indices)
    shuffle(name_indices)
    st.names.clear()
    st.images.clear()
    st.cycle += 1
    st.state = st.ST_SHOW


# ---------------------------------------------------------------------------
def show_image():

    global img_count

    if img_count == 0:
        img_count = 0
        shuffle(st.names)
        shuffle(st.images)
        st.state = st.ST_WAIT
        st.image = st.images[img_count]
        paint()

    else:
        img_idx = img_indices[img_count]
        name_idx = name_indices[img_count]
        st.image, gender = FACES[img_idx]
        if gender == st.FEMALE:
            st.name = FEMALE_NAMES[name_idx]
        else:
            st.name = MALE_NAMES[name_idx]
        st.names.append((st.image, st.name))
        st.images.append(st.image)
        paint()

        img_count -= 1


# ---------------------------------------------------------------------------
def check(xy):
    global img_count, round_score

    name_idx = get_name_idx(xy)
    image = st.names[name_idx][0]
    if image == st.image:
        st.score += 1
        round_score += 1

    img_count += 1
    if img_count == st.level:
        st.total += st.level
        st.delay = 7
        st.state = st.ST_COUNT
        if round_score == st.level:
            st.level += 1
        paint_status(0)
    else:
        st.image = st.images[img_count]
        paint()
