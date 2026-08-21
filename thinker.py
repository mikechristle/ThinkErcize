#!/usr/bin/python
# ---------------------------------------------------------------------------
# Thinker
# Game to exercise your thinker
# Mike Christle 2022
# ---------------------------------------------------------------------------

import tkinter as tk
import json

from os import chdir
from subprocess import Popen, PIPE

BLUE = '#0000FF'
BLACK = '#000000'
GREEN = '#008000'
FONT0 = "Helvetica 24 underline"
FONT1 = "Helvetica 24"

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

game_scores = {
    "best_route": [0, 0, 0, 0],           # Level Miles
    "digit_order": [0, 0],                # Score
    "laser_path": [0, 0],                 # Score
    "math_test": [0, 100.0, 0, 100.0],    # Score Time
    "maze_escape": [100.0, 100.0],        # Time
    "maze_spinner": [100.0, 100.0],       # Time
    "memory_patterns": [0, 0],            # Score
    "origami": [0, 100.0, 0, 100.0],      # Score Time
    "thats_new": [0, 0],                  # Score
    "tile_match": [100.0, 100.0],         # Time
    "train_of_thought": [0, 0, 0, 0],     # Level Trains
    "which_arrow": [0, 100.0, 0, 100.0],  # Score Time
    "word_color": [0, 100.0, 0, 100.0],   # Score Time
}

root: tk.Tk

# ---------------------------------------------------------------------------
def run(path, command):
    """Run a game program."""

    root.iconify()
    chdir(path)

    with Popen(
        command,
        stdout=PIPE,
        stderr=PIPE,
        text=True,
    ) as process:
        process.wait()
        stdout, stderr = process.communicate()

    if len(stderr) > 0:
        print(f'STDERR: {stderr}')
    else:
        update_score(stdout.split('\n'))

    chdir('..')
    root.deiconify()


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
def update_score(scores):
    """Update the score after each game."""

    for idx in range(2, len(scores)):
        result = scores[idx].split(' ')
        if len(result) < 2:
            continue

        game = result[0]
        old_score = game_scores[game]
        match game:
            case 'best_route':
                level = int(result[1])
                least = int(result[2])
                score = int(result[3]) - least
                ll, ls, bl, bs = game_scores[game]
                if score < bs or level > bl:
                    bs = score
                    bl = level
                game_scores[game] = level, score, bl, bs

            case 'math_test' | 'origami' | 'which_arrow' | 'word_color':
                score = int(result[1])
                time = float(result[2])
                ls, lt, bs, bt = game_scores[game]
                if score > bs or score == bs and time < bt:
                    bs, bt = score, time
                game_scores[game] = score, time, bs, bt

            case 'maze_escape' | 'maze_spinner' | 'tile_match':
                score = float(result[1])
                ls, bs = game_scores[game]
                if score < bs:
                    bs = score
                game_scores[game] = score, bs

            case 'train_of_thought':
                level = int(result[1])
                score = int(result[2])
                ll, ls, bl, bs = game_scores[game]
                if level > bl or score > bs:
                    bl, bs = level, score
                game_scores[game] = bl, bs, level, score

            case _:
                score = int(result[1])
                ls, bs = game_scores[game]
                if score > bs:
                    bs = score
                game_scores[game] = score, bs


# ---------------------------------------------------------------------------
def format_score(game, score):
    match game:
        case 'best_route':
            return f' {game:17} Level {score[0]}   Extra Miles {score[1]:<3}   Level {score[2]}   Extra Miles {score[3]}\n'
        case 'train_of_thought':
            return f' {game:17} Level {score[0]}   Trains {score[1]:<3}        Level {score[2]}   Trains {score[3]}\n'
        case 'math_test' | 'origami' | 'which_arrow' | 'word_color':
            return f' {game:17} Score {score[0]:<3} Time {score[1]:5.1f} Sec    Score {score[2]:<3} Time {score[3]:5.1f} Sec\n'
        case 'maze_escape' | 'maze_spinner' | 'tile_match':
            return f' {game:17} Time {score[0]:5.1f} Sec              Time {score[1]:5.1f} Sec\n'

    return f' {game:17} Score {score[0]:<4}                  Score {score[1]}\n'


# ---------------------------------------------------------------------------
def view_scores(_):

    child = tk.Toplevel(root)
    child.title("View Scores")

    text_box = tk.Text(child,
                       height=14, width=72,
                       font=("Courier New", 20))
    text_box.pack(padx=10, pady=10)
    text_box.tag_configure("bold", font=("Courier New", 20, "bold"))
    text_box.insert(tk.END, '                   Last Game                   Best Game\n', 'bold')
    for key, value in game_scores.items():
        text_box.insert('end', format_score(key, value))
    text_box.config(state="disabled")


# ---------------------------------------------------------------------------
def main():
    """Main program."""

    global root, game_scores

    # Set up the window
    root = tk.Tk()
    root.title('Thinker Exercises   V1.2')
    root.geometry('800x380')
    root.resizable(False, False)

    lbl0 = tk.Label(root, text='Memory', font=FONT0, fg=GREEN)
    lbl0.grid(column=0, row=0, pady=5, padx=10)

    lbl1 = tk.Label(root, text='Concentration', font=FONT0, fg=GREEN)
    lbl1.grid(column=1, row=0, pady=5, padx=10)

    lbl2 = tk.Label(root, text='Problem Solving', font=FONT0, fg=GREEN)
    lbl2.grid(column=2, row=0, pady=5, padx=10)

    # Add a label for each game
    for name in GAME_NAMES:
        lbl = tk.Label(
            root,
            text=name[0],
            font=FONT1,
            fg=BLACK,
            name=name[1],
        )
        lbl.grid(column=name[2], row=name[3], pady=5, padx=10)
        lbl.bind("<Button-1>", handle_click)
        lbl.bind('<Enter>', enter)
        lbl.bind('<Leave>', leave)

    # View scores button
        lbl = tk.Label(
            root,
            text='View Scores',
            font=FONT1,
            fg=BLACK,
        )
        lbl.grid(column=2, row=6, pady=5, padx=10)
        lbl.bind("<Button-1>", view_scores)
        lbl.bind('<Enter>', enter)
        lbl.bind('<Leave>', leave)

    # Read game scores
    try:
        with open('scores.json', 'r') as file:
            game_scores = json.load(file)

    # If file not created, use default values
    except FileNotFoundError:
        pass

    # Enter tkinter event loop
    root.mainloop()

    # Save game scores
    with open("scores.json", "w") as file:
        json.dump(game_scores, file)


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
