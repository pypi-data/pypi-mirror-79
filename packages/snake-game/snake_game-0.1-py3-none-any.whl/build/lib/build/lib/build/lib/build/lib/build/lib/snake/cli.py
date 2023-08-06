import argparse

from snake.main import run


def main():
    parser = argparse.ArgumentParser('Snake Game.')
    parser.add_argument('-s', '--start', help='start game', action='store_true')

    args = parser.parse_args()

    if args.start:
        run()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
