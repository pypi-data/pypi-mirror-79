import threading

from readchar import key, readkey
from snake.constants import Direction


def take_input(direction):
    while True:
        key_pressed = readkey()

        key_to_direction = {
            key.LEFT: Direction.LEFT,
            key.RIGHT: Direction.RIGHT,
            key.UP: Direction.UP,
            key.DOWN: Direction.DOWN,
        }

        new_direction = key_to_direction.get(key_pressed, direction[0])

        if not Direction.are_opposite(direction[0], new_direction):
            direction[0] = key_to_direction.get(key_pressed, direction[0])


def capture_key_press(direction):
    thread = threading.Thread(
        target=take_input, args=(direction,), daemon=True
    )
    thread.start()
