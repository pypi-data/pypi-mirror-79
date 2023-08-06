class Direction:
    RIGHT = 'r'
    LEFT = 'l'
    UP = 'u'
    DOWN = 'd'

    @staticmethod
    def are_opposite(first, second):
        opposite_directions = [
            {Direction.LEFT, Direction.RIGHT},
            {Direction.UP, Direction.DOWN},
        ]
        if {first, second} in opposite_directions:
            return True
