import os


class Board():
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.initialize()

    @staticmethod
    def _clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw(self):
        Board._clear_screen()
        for row in self._board:
            for cell in row:
                print(cell, end='')
            print('')

    def initialize(self):
        height = self.height
        width = self.width

        board = [[' ' for i in range(width)] for j in range(height)]

        for i in range(len(board)):
            for j in range(len(board[i])):
                if i == 0 or i == height - 1:
                    board[i][j] = '─'
                elif j == 0 or j == width - 1:
                    board[i][j] = '│'

        board[0][0] = '┌'
        board[0][width - 1] = '┐'
        board[height - 1][0] = '└'
        board[height - 1][width - 1] = '┘'

        self._board = board

    def set(self, x, y, val):
        self._board[x][y] = val


'''
Unicode characters for drawing rectangles
┌─────────┐
│         │
│         │
│         │
│         │
└─────────┘
'''
