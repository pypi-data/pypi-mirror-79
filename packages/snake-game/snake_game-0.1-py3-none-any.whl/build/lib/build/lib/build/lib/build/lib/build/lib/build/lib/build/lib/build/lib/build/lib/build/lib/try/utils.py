import sys
import tty
import termios


def getch(char_width=1):
    '''get a fixed number of typed characters from the terminal.
    Linux / Mac only'''
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        ch = sys.stdin.read(char_width)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
