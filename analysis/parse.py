__author__ = 'elvijs'

NON_PRAWNS = {"N", "B", "R", "Q", "K"}


class MoveIsCastle(Exception):
    def __init__(self, move):
        self.move = move


def parse_move(move_string):
    """
    Remove checks and raise castle exceptions.
    """
    if move_string in ["0-0", "0-0-0"]:
        raise MoveIsCastle(move_string)

    if move_string[0] in NON_PRAWNS:
        piece = move_string[0].lower()
    else:
        piece = "p"

    if move_string[-1] == "+":
        target_square = move_string[-3:-1]
    else:
        target_square = move_string[-2:]

    return piece, target_square
