import random

from snake.board import Board
from snake.constants import Direction
from snake.player_input import capture_key_press
from snake.snake import InvalidMove, Snake


class Game:

    def __init__(self):
        self.direction = [Direction.RIGHT]
        capture_key_press(self.direction)

        self.board = Board(15, 40)
        self.snake = Snake(pos=(1, 1))
        self.food = []
        self._insert_food()

    def start(self):
        while True:
            self.board.draw()

            try:
                self.snake.move(self.board, self.direction[0], self.food)
                if not self.food:
                    self._insert_food()
            except InvalidMove:
                print('Game Over.')
                break

    def _insert_food(self):
        x, y = self._get_food_location()
        while (x, y) in self.snake.positions:
            x, y = self._get_food_location()
        self.food.append((x, y))
        self.board.set(x, y, '*')

    def _get_food_location(self):
        # x = random.randint(1, self.board.height - 2)
        # y = random.choice([i for i in range(1, self.board.width - 2, 2)])
        x = random.randint(5, self.board.height - 5)
        y = random.choice([i for i in range(5, self.board.width - 5, 2)])
        return x, y
