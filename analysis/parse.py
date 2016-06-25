import logging

__author__ = 'elvijs'

logger = logging.getLogger("Move parser")

CHESS_PIECES = {"p", "n", "b", "r", "q", "k"}
CHESS_SQUARE_LETTERS = {"a", "b", "c", "d", "e", "f", "g", "h"}
CHESS_SQUARE_NUMBERS = {"1", "2", "3", "4", "5", "6", "7", "8"}
NON_PRAWNS = {"N", "B", "R", "Q", "K"}
CASTLE_MOVES = ["O-O", "O-O-O", "O-O+", "O-O-O+"]
ALLOWED_COLOURS = {"b", "w"}


def get_move_landing_squares(move_string, colour):
    """
    Remove checks, parse promotion.
    :move_string: a move string to be parsed e.g. "Nb1", "Qxb4++",
    :colour: should be either "w" or "b".
    """
    assert colour in ALLOWED_COLOURS

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


def get_move_description(move_string, board, colour):
    """
    Get a full move description dictionary object of the following schema:
    {
        "move_string": "Nxc3++"
        "piece_movements": [
            {
                "piece": "nb1",
                "from": "b1",
                "to": "c3"
            }
        ],
        "check": true,
        "capture": true,
        "checkmate": true
    }
    :param move_string:
    :param board: a dict describing the board this move should be performed on.
    :return:
    """
    assert colour in ALLOWED_COLOURS


def get_board(move_descriptions):
    ret = get_initial_board()
    for m in move_descriptions:
        update_board(ret, m)
    return ret


def update_board(current_board, move_description):
    for pm in move_description['piece_movements']:
        current_board[pm['to']] = current_board[pm['from']]
        current_board[pm['from']] = None


def get_initial_board():
    """
    :return: a dict of (key, value) pairs, where key is the square and
    value is the unique identifier for a piece.
    """
    return dict(
        a1="ra1", a2="pa2", a3=None, a4=None, a5=None, a6=None, a7="pa7", a8="ra8",
        b1="nb1", b2="pb2", b3=None, b4=None, b5=None, b6=None, b7="pb7", b8="nb8",
        c1="bc1", c2="pc2", c3=None, c4=None, c5=None, c6=None, c7="pc7", c8="bc8",
        d1="qd1", d2="pd2", d3=None, d4=None, d5=None, d6=None, d7="pd7", d8="qd8",
        e1="ke1", e2="pe2", e3=None, e4=None, e5=None, e6=None, e7="pe7", e8="kd8",
        f1="bf1", f2="pf2", f3=None, f4=None, f5=None, f6=None, f7="pf7", f8="bf8",
        g1="ng1", g2="pg2", g3=None, g4=None, g5=None, g6=None, g7="pg7", g8="ng8",
        h1="rh1", h2="ph2", h3=None, h4=None, h5=None, h6=None, h7="ph7", h8="rh8"
    )
