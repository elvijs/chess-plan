import logging

__author__ = 'elvijs'

logger = logging.getLogger("Move parser")

CHESS_PIECES = {"p", "n", "b", "r", "q", "k"}
CHESS_SQUARE_LETTERS = {"a", "b", "c", "d", "e", "f", "g", "h"}
CHESS_SQUARE_NUMBERS = {"1", "2", "3", "4", "5", "6", "7", "8"}
NON_PRAWNS = {"N", "B", "R", "Q", "K"}
CASTLE_MOVES = ["O-O", "O-O-O", "O-O+", "O-O-O+"]


def get_move_landing_squares(move_string, colour):
    """
    Remove checks, parse promotion.
    :move_string: a move string to be parsed e.g. "Nb1", "Qxb4++",
    :colour: should be either "w" or "b".
    """
    if move_string in CASTLE_MOVES:
        if colour == "w":
            if move_string == "O-O":
                return [("k", "g1"), ("r", "f1")]
            else:
                return [("k", "c1"), ("r", "d1")]
        else:
            if move_string == "O-O":
                return [("k", "g8"), ("r", "f8")]
            else:
                return [("k", "c8"), ("r", "d8")]

    if move_string[0] in NON_PRAWNS:
        piece = move_string[0].lower()
    else:
        piece = "p"

    if move_string[-1] in {"+"}.union(NON_PRAWNS):
        target_square = move_string[-3:-1]
    else:
        target_square = move_string[-2:]

    try:
        assert piece in CHESS_PIECES
        assert target_square[0] in CHESS_SQUARE_LETTERS
        assert target_square[1] in CHESS_SQUARE_NUMBERS
    except AssertionError:
        logger.debug("AssertionError whilst parsing {}".format(move_string))
        return [(None, None)]

    return [(piece, target_square)]
