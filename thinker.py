# ---------------------------------------------------------------------------
# Thinker
# Game to exercise your thinker
# Mike Christle 2022
# ---------------------------------------------------------------------------

import sys
import os
import pygame

IMAGE_WIDTH = 400
IMAGE_HEIGHT = 400
LINE_SEPERATION = 60

pygame.init()
screen = pygame.display.set_mode((IMAGE_WIDTH, IMAGE_HEIGHT))
pygame.display.set_caption('Thinker Exercises   V1.0')

BG_COLOR = 107, 142, 35
TEXT_COLOR = (255, 255, 255)
NAME_FONT = pygame.font.SysFont('Arial', 48)
GAME_NAMES = (
    'Laser Path',
    'Maze Spinner',
    'Origami',
    'That\' New',
    'Train of Thought',
)

# Paint the game titles
screen.fill(BG_COLOR)
y = LINE_SEPERATION // 2
for line in GAME_NAMES:
    text = NAME_FONT.render(line, True, TEXT_COLOR)
    rect = text.get_rect()
    rect.center = (IMAGE_WIDTH // 2, y)
    screen.blit(text, rect)
    y += LINE_SEPERATION

pygame.display.update()

while True:

    # Get all pygame events
    for event in pygame.event.get():
        match event.type:

            # Exit if window is closed
            case pygame.QUIT:
                sys.exit()

            # Player has clicked on a game title
            case pygame.MOUSEBUTTONDOWN:
                xy = event.pos
                match xy[1] // LINE_SEPERATION:
                    case 0:
                        os.chdir('LaserPath')
                        os.system('python laser_path.py')
                        os.chdir('..')
                    case 1:
                        os.chdir('MazeSpinner')
                        os.system('python maze_spinner.py')
                        os.chdir('..')
                    case 2:
                        os.chdir('Origami')
                        os.system('python origami.py')
                        os.chdir('..')
                    case 3:
                        os.chdir('ThatsNew')
                        os.system('python thats_new.py')
                        os.chdir('..')
                    case 4:
                        os.chdir(r'TrainOfThought')
                        os.system(r'python train_of_thought.py')
                        os.chdir('..')
