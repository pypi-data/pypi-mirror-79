import time
import threading
# import getch
# from utils import getch
import readchar
from readchar import key

KEY = ''


def take_input():
    global KEY
    while True:
        # x = getch()
        # x = readchar.readchar()
        x = readchar.readkey()
        print('Input:', x)
        if x == key.RIGHT:
            print('right')
        if x == 'q':
            return
        with threading.Lock():
            KEY = x


def main():
    thread = threading.Thread(target=take_input, daemon=True)
    thread.start()

    for i in range(5):
        print('Hi', KEY)
        time.sleep(1)


main()
