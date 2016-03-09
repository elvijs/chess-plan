__author__ = 'elvijs'

NON_PRAWNS = {"N", "B", "R", "Q", "K"}


class MoveParsingException(Exception):
    def __init__(self, move, error):
        self.move = move
        self.error = error

    def __str__(self):
        return "error parsing move {0}, error '{1}'".format(self.move, self.error)


def parse_move(move_string):
    """
    Remove checks and parse castles.
    """
    if move_string in ["0-0", "0-0-0"]:
        raise MoveParsingException(move_string, "Not implemented yet")

    if move_string[0] in NON_PRAWNS:
        piece = move_string[0].lower()
    else:
        piece = "p"

    if move_string[-1] == "+":
        target_square = move_string[-3:-1]
    else:
        target_square = move_string[-2:]

    return piece, target_square
