#!/usr/bin/python
# ---------------------------------------------------------------------------
# Thinker
# Game to exercise your thinker
# Mike Christle 2022
# ---------------------------------------------------------------------------

import tkinter as tk

from os import chdir
from subprocess import Popen

BLUE = '#0000FF'
BLACK = '#000000'
GREEN = '#008000'
FONT0 = ("Helvetica 24 underline")
FONT1 = ("Helvetica 24")

GAME_NAMES = (
    # Memory
    ('Laser Path', 'lp', 0, 1),
    ('That\'s New', 'tn', 0, 2),
    ('Memory Patterns', 'mp', 0, 3),
    ('Digit Order', 'do', 0, 4),

    # Concentration
    ('Maze Spinner', 'ms', 1, 1),
    ('Train of Thought', 'tt', 1, 2),
    ('Word Color', 'wc', 1, 3),
    ('Tile Match', 'tm', 1, 4),
    ('Which Arrow', 'wa', 1, 5),

    # Problem Solving
    ('Maze Escape', 'me', 2, 1),
    ('Origami', 'or', 2, 2),
    ('Best Route', 'bm', 2, 3),
    ('Math Test', 'mt', 2, 4),
)


# ---------------------------------------------------------------------------
def run(path, command):
    """Run a game program."""

    window.iconify()
    chdir(path)

    with Popen(command) as process:
        process.wait()

    chdir('..')
    window.deiconify()


# ---------------------------------------------------------------------------
def handle_click(event):
    """Handle a user click event."""

    match str(event.widget):
        case '.lp': run('LaserPath', 'python laser_path.py')
        case '.ms': run('MazeSpinner', 'python maze_spinner.py')
        case '.me': run('MazeEscape', 'python maze_escape.py')
        case '.or': run('Origami', 'python origami.py')
        case '.tn': run('ThatsNew', 'python thats_new.py')
        case '.tt': run('TrainOfThought', 'python train_of_thought.py')
        case '.mp': run('MemoryPatterns', 'python memory_patterns.py')
        case '.do': run('DigitOrder', 'python digit_order.py')
        case '.wc': run('WordColor', 'python word_color.py')
        case '.tm': run('TileMatch', 'python tile_match.py')
        case '.bm': run('BestRoute', 'python best_route.py')
        case '.wa': run('WhichArrow', 'python which_arrow.py')
        case '.mt': run('MathTest', 'python math_test.py')


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

    global window

    # Setup the window
    window = tk.Tk()
    window.title('Thinker Exercises   V1.1')
    window.geometry('800x380')
    window.resizable(False, False)

    lbl0 = tk.Label(window, text='Memory', font=FONT0, fg=GREEN)
    lbl0.grid(column=0, row=0, pady=5, padx=10)

    lbl1 = tk.Label(window, text='Concentration', font=FONT0, fg=GREEN)
    lbl1.grid(column=1, row=0, pady=5, padx=10)

    lbl2 = tk.Label(window, text='Problem Solving', font=FONT0, fg=GREEN)
    lbl2.grid(column=2, row=0, pady=5, padx=10)

    # Add a label for each game
    for name in GAME_NAMES:
        lbl = tk.Label(
            window,
            text=name[0],
            font=FONT1,
            fg=BLACK,
            name=name[1],
        )
        lbl.grid(column=name[2], row=name[3], pady=5, padx=10)
        lbl.bind("<Button-1>", handle_click)
        lbl.bind('<Enter>', enter)
        lbl.bind('<Leave>', leave)

    # Enter tkinter event loop
    window.mainloop()


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
