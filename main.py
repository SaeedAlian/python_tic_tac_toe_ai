import sys
import pygame
import copy
import random
import numpy

from constants import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)


class Square:
    def __init__(self, col: int, row: int):
        self.col = col
        self.row = row
        self.state = 0

    def draw(self):
        posX = self.col * SQSIZE
        posY = self.row * SQSIZE
        width = SQSIZE if self.col + 1 == COLS else SQSIZE - SQUARE_MARGIN
        height = SQSIZE if self.row + 1 == ROWS else SQSIZE - SQUARE_MARGIN

        pygame.draw.rect(
            screen,
            SQUARE_COLOR,
            (
                posX,
                posY,
                width,
                height
            )
        )

    def set_state(self, state: int, draw=True):
        if self.state != 0 and state != 0:
            return

        self.state = state

        if not draw:
            return

        match self.state:
            case 0:
                # Draw an empty square if state is 0
                self.draw()

            case 1:
                # Draw a cross for player 1
                self.__draw_cross()

            case 2:
                # Draw a circle for player 2
                self.__draw_circle()

    def __draw_circle(self):
        centerCoordinates = (self.col * SQSIZE + (SQSIZE // 2) - CENTER_OFFSET,
                             self.row * SQSIZE + (SQSIZE // 2) - CENTER_OFFSET)

        pygame.draw.circle(screen, CIRCLE_COLOR,
                           centerCoordinates, CIRCLE_RADIUS, CIRCLE_WIDTH)

    def __draw_cross(self):
        self.__draw_descending_line()
        self.__draw_ascending_line()

    def __draw_descending_line(self):
        descendingLineStart = (self.col * SQSIZE + CROSS_OFFSET - CENTER_OFFSET,
                               self.row * SQSIZE + CROSS_OFFSET - CENTER_OFFSET)

        descendingLineEnd = (self.col * SQSIZE + SQSIZE - CROSS_OFFSET - CENTER_OFFSET,
                             self.row * SQSIZE + SQSIZE - CROSS_OFFSET - CENTER_OFFSET)

        pygame.draw.line(screen, CROSS_COLOR, descendingLineStart,
                         descendingLineEnd, CROSS_WIDTH)

    def __draw_ascending_line(self):
        ascendingLineStart = (self.col * SQSIZE + SQSIZE - CROSS_OFFSET - CENTER_OFFSET,
                              self.row * SQSIZE + CROSS_OFFSET - CENTER_OFFSET)

        ascendingLineEnd = (self.col * SQSIZE + CROSS_OFFSET - CENTER_OFFSET,
                            self.row * SQSIZE + SQSIZE - CROSS_OFFSET - CENTER_OFFSET)

        pygame.draw.line(screen, CROSS_COLOR, ascendingLineStart,
                         ascendingLineEnd, CROSS_WIDTH)


class Board:
    def __init__(self):
        self.squares = numpy.ndarray((ROWS, COLS), dtype='object')
        self.marked_squares = 0

    def assign_squares(self):
        for (col, row), value in numpy.ndenumerate(self.squares):
            self.squares[col][row] = Square(col, row)

    def draw_squares(self):
        for (col, row), square in numpy.ndenumerate(self.squares):
            square.draw()

    def mark_square(self, col, row, player, draw=True):
        self.squares[col][row].set_state(player, draw)
        self.marked_squares += 1

    def check_final_state(self, draw_line=False) -> int:
        '''
            @return 0 if none the players won
            @return 1 if player 1 has won
            @return 2 if player 2 has won
        '''

        # Vertical check
        for row in range(ROWS):
            if self.squares[row][0].state == self.squares[row][1].state == self.squares[row][2].state != 0:
                if draw_line:
                    self.draw_winning_line(
                        self.squares[row][0].state, "vertical", 0, row)
                return self.squares[row][0].state

        # Horizontal check
        for col in range(COLS):
            if self.squares[0][col].state == self.squares[1][col].state == self.squares[2][col].state != 0:
                if draw_line:
                    self.draw_winning_line(
                        self.squares[0][col].state, "horizontal", col, 0)
                return self.squares[0][col].state

        # Descending diagonal check
        if self.squares[0][0].state == self.squares[1][1].state == self.squares[2][2].state != 0:
            if draw_line:
                self.draw_winning_line(
                    self.squares[1][1].state, "desc_diagonal")
            return self.squares[1][1].state

        # Ascending diagonal check
        if self.squares[0][2].state == self.squares[1][1].state == self.squares[2][0].state != 0:
            if draw_line:
                self.draw_winning_line(
                    self.squares[1][1].state, "asc_diagonal")
            return self.squares[1][1].state

        # if none of the players have won
        return 0

    def draw_winning_line(self, player: int, direction: str, col=0, row=0):
        match direction:
            case "vertical":
                startPos = (row * SQSIZE + SQSIZE // 2 - CENTER_OFFSET,
                            SQUARE_MARGIN)
                endPos = (row * SQSIZE + SQSIZE // 2 - CENTER_OFFSET,
                          (ROWS) * SQSIZE - SQUARE_MARGIN)
            case "horizontal":
                startPos = (SQUARE_MARGIN, col * SQSIZE +
                            SQSIZE // 2 - CENTER_OFFSET)
                endPos = ((COLS) * SQSIZE - SQUARE_MARGIN, col *
                          SQSIZE + SQSIZE // 2 - CENTER_OFFSET)
            case "desc_diagonal":
                startPos = (SQUARE_MARGIN, SQUARE_MARGIN)
                endPos = ((COLS - 1) * SQSIZE + SQSIZE - SQUARE_MARGIN,
                          (ROWS - 1) * SQSIZE + SQSIZE - SQUARE_MARGIN)
            case "asc_diagonal":
                startPos = ((COLS - 1) * SQSIZE + SQSIZE -
                            SQUARE_MARGIN - CENTER_OFFSET, SQUARE_MARGIN - CENTER_OFFSET)
                endPos = (SQUARE_MARGIN - CENTER_OFFSET,
                          (ROWS - 1) * SQSIZE + SQSIZE - SQUARE_MARGIN - CENTER_OFFSET)

        color = CROSS_COLOR if player == 1 else CIRCLE_COLOR

        pygame.draw.line(screen, color, startPos, endPos, LINE_WIDTH)

    def get_empty_squares(self):
        empty_sqrs = []

        for (col, row), square in numpy.ndenumerate(self.squares):
            if square.state == 0:
                empty_sqrs.append(square)

        return empty_sqrs

    def is_full(self) -> bool:
        return self.marked_squares == ROWS * COLS

    def is_empty(self) -> bool:
        return self.marked_squares == 0


class AI:
    def __init__(self, level=0, player=2):
        self.player = player
        self.level = level

    def random_selection(self, board):
        empty_squares = board.get_empty_squares()
        index = random.randrange(0, len(empty_squares))

        return empty_squares[index]

    def minimax(self, board: Board, maximizing: bool) -> tuple[int, Square]:
        '''
            @return (eval, square)
        '''
        terminal_case = board.check_final_state()

        if terminal_case == 1:
            return 1, None

        if terminal_case == 2:
            return -1, None

        if board.is_full():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move_square = None
            empty_squares = board.get_empty_squares()

            for square in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(
                    square.col, square.row, 1, False)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move_square = square

            return max_eval, best_move_square

        else:
            min_eval = 100
            best_move_square = None
            empty_squares = board.get_empty_squares()

            for square in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(
                    square.col, square.row, 2, False)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move_square = square

            return min_eval, best_move_square

    def eval(self, board: Board):
        if self.level == 0:
            # Random
            eval = "random"
            square = self.random_selection(board)
        else:
            # Minimax
            eval, square = self.minimax(board, False)

        print(
            f'AI has chosen to mark the square in pos ({square.col}, {square.row}) with an eval of: {eval}')

        return square


class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 2  # 1 is cross, 2 is circle
        self.game_mode = "ai"  # pvp | ai
        self.is_ended = False

        self.board.assign_squares()
        self.board.draw_squares()

    def make_move(self, col: int, row: int):
        self.board.mark_square(col, row, self.player)
        self.change_player()
        self.is_over()

    def change_player(self):
        self.player = self.player % 2 + 1

    def is_over(self) -> bool:
        is_ended = self.board.check_final_state(
            True) != 0 or self.board.is_full()
        self.is_ended = is_ended
        return is_ended

    def reset(self):
        self.__init__()


def main():
    game = Game()

    # Mainloop
    while True:
        for event in pygame.event.get():
            # Quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Keydown events
            if event.type == pygame.KEYDOWN:
                # r for restart
                if event.key == pygame.K_r:
                    screen.fill(BG_COLOR)
                    game.reset()

            # Mouse down event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game.is_ended and event.button == 1:
                    pos = event.pos
                    row = pos[1] // SQSIZE
                    col = pos[0] // SQSIZE

                    game.make_move(col, row)

        # AI move
        if game.game_mode == "ai" and game.player == 2 and not game.is_ended:
            pygame.display.update()
            square = game.ai.eval(game.board)
            game.make_move(square.col, square.row)

            # Change random move to minimax algo for AI
            if game.ai.level != 1:
                game.ai.level = 1

        pygame.display.update()


main()
