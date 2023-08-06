import time

from snake.constants import Direction


class InvalidMove(Exception):
    pass


class Snake:

    def __init__(self, pos):
        self.positions = [pos]

    def _get_next_head_pos(self, direction):
        head = self.positions[-1]

        if direction == Direction.RIGHT:
            head = (head[0], head[1] + 2)
        elif direction == Direction.LEFT:
            head = (head[0], head[1] - 2)
        elif direction == Direction.UP:
            head = (head[0] - 1, head[1])
        elif direction == Direction.DOWN:
            head = (head[0] + 1, head[1])
        return head

    def _validate_move(self, head, board):
        if (
            head[0] <= 0 or head[0] >= board.height - 1 or
            head[1] <= 0 or head[1] >= board.width - 1
        ):
            raise InvalidMove()

    def move(self, board, direction, food):
        head = self._get_next_head_pos(direction)
        self._validate_move(head, board)

        self.positions.append(head)

        if head not in food:
            tail = self.positions.pop(0)
            board.set(tail[0], tail[1], ' ')
        else:
            food.pop()

        head = self.positions[-1]
        board.set(head[0], head[1], 's')

        time.sleep(0.14)
