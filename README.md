# Tic Tac Toe AI

## Requirements

-   Python 3
-   Pygame
-   Autopep8
-   Numpy
-   Pycodestyle=
-   Tomli
-   Pip package manager

## Getting started

First clone or download the repository, then run the command below inside the project directory :

`pip install -r requirements.txt`

When the installation is finished run this command to start the game :

`python3 main.py`

## Restart the game

Press R key to restart the game.

## Code structure

### Folders and files

-   .gitignore
-   constants.py
-   main.py
-   README.md
-   requirements.txt

### Constants

```
WIDTH : int : default = 600
HEIGHT : int : default = 600

ROWS : int : default = 3
COLS : int : default = 3
SQSIZE : int : default = WIDTH // COLS

SQUARE_MARGIN : int : default = 10
CIRCLE_WIDTH : int : default = 15
CROSS_WIDTH : int : default = 20
LINE_WIDTH : int : default = 15

CIRCLE_RADIUS : int : default = SQSIZE // 4 + 10

CROSS_OFFSET : int : default = 40
CENTER_OFFSET : int : default = 5

# COLORS
BG_COLOR : tuple : default = (41, 118, 37)
SQUARE_COLOR : tuple : default = (69, 167, 64)
CIRCLE_COLOR : tuple : default = (239, 231, 200)
CROSS_COLOR : tuple : default = (66, 66, 66)
```

## Changing the game mode

For changing the game mode you must change the game_mode option in the Game class to "pvp" for player vs player or "ai" for player vs ai.
