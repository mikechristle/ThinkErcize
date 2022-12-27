#!/usr/bin/python
# ---------------------------------------------------------------------------
# Thinker
# Game to exercise your thinker
# Mike Christle 2022
# ---------------------------------------------------------------------------

import os
import tkinter as tk

from subprocess import Popen

BLUE = '#0000FF'
BLACK = '#000000'
FONT = ("Helvetica", 24)

GAME_NAMES = (
    ('Laser Path', 'lp'),
    ('Maze Spinner', 'ms'),
    ('Origami', 'or'),
    ('That\'s New', 'tn'),
    ('Train of Thought', 'tt'),
    ('Memory Patterns', 'mp'),
    ('Digit Order', 'do'),
    ('Word Color', 'wc'),
    ('Tile Match', 'tm'),
    ('Best Route', 'bm'),
)


# ---------------------------------------------------------------------------
def run(path, command):
    """Run a game program."""

    os.chdir(path)
    Popen(command)
    os.chdir('..')


# ---------------------------------------------------------------------------
def handle_click(event):
    """Handle a user click event."""

    match str(event.widget):
        case '.lp': run('LaserPath', 'python laser_path.py')
        case '.ms': run('MazeSpinner', 'python maze_spinner.py')
        case '.or': run('Origami', 'python origami.py')
        case '.tn': run('ThatsNew', 'python thats_new.py')
        case '.tt': run('TrainOfThought', 'python train_of_thought.py')
        case '.mp': run('MemoryPatterns', 'python memory_patterns.py')
        case '.do': run('DigitOrder', 'python digit_order.py')
        case '.wc': run('WordColor', 'python word_color.py')
        case '.tm': run('TileMatch', 'python tile_match.py')
        case '.bm': run('BestRoute', 'python best_route.py')


# ---------------------------------------------------------------------------
def enter(event):
    """Change text color when mouse hovers over label."""

    event.widget['fg'] = BLUE


# ---------------------------------------------------------------------------
def leave(event):
    """Restore text color when mouse leaves label."""

    event.widget['fg'] = BLACK


# ---------------------------------------------------------------------------
def main():
    """Main program."""

    # Setup the window
    window = tk.Tk()
    window.title('Thinker Exercises')
    window.geometry('300x400+50+50')
    window.resizable(False, False)

    # Add a label for each game
    for name in GAME_NAMES:
        lbl = tk.Label(
            window,
            text=name[0],
            font=FONT,
            fg=BLACK,
            name=name[1],
        )
        lbl.pack()
        lbl.bind("<Button-1>", handle_click)
        lbl.bind('<Enter>', enter)
        lbl.bind('<Leave>', leave)

    # Enter tkinter event loop
    window.mainloop()


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
