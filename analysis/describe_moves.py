from analysis import ALLOWED_COLOURS, CASTLE_MOVES, PIECES, PIECE_IDENTIFIERS, SQUARE_LETTERS, SQUARE_NUMBERS, logger

__author__ = 'elvijs'


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
    return dict(
        move_string=move_string,
        check=is_check(move_string),
        capture=is_capture(move_string),
        checkmate=is_checkmate(move_string),
        piece_movements=get_piece_movements(move_string, board, colour)
    )


def get_piece_movements(move_string, board, colour):
    assert colour in ALLOWED_COLOURS

    if move_string in CASTLE_MOVES:
        return get_piece_movements_in_castle(move_string, colour)

    piece_letter = get_piece_letter(move_string)
    to_square = get_to_square(move_string)
    from_square = get_from_square(piece_letter, to_square, board)
    piece = board[from_square]

    try:
        assert piece_letter in PIECES
        assert piece in PIECE_IDENTIFIERS
        assert to_square[0] in SQUARE_LETTERS
        assert to_square[1] in SQUARE_NUMBERS
        assert from_square[0] in SQUARE_LETTERS
        assert from_square[1] in SQUARE_NUMBERS
    except AssertionError:
        logger.debug("AssertionError whilst parsing {}".format(move_string))

    return {
        "to": to_square,
        "from": from_square,
        "piece": piece
    }


def get_piece_movements_in_castle(move_string, colour):
    if colour == "w":
        if move_string == "O-O":
            return [
                {
                    "piece": "ke1",
                    "from": "e1",
                    "to": "g1"
                },
                {
                    "piece": "rh1",
                    "from": "h1",
                    "to": "f1"
                }
            ]
        else:
            return [
                {
                    "piece": "ke1",
                    "from": "e1",
                    "to": "c1"
                },
                {
                    "piece": "ra1",
                    "from": "a1",
                    "to": "d1"
                }
            ]
    else:
        if move_string == "O-O":
            return [
                {
                    "piece": "ke8",
                    "from": "e8",
                    "to": "g8"
                },
                {
                    "piece": "rh8",
                    "from": "h8",
                    "to": "f8"
                }
            ]
        else:
            return [
                {
                    "piece": "ke8",
                    "from": "e8",
                    "to": "c8"
                },
                {
                    "piece": "ra8",
                    "from": "a8",
                    "to": "d8"
                }
            ]


def get_piece_letter(move_string):
    pass


def get_to_square(move_string):
    pass


def get_from_square(piece_letter, to_square, board):
    pass


def is_check(move_string):
    pass


def is_capture(move_string):
    pass


def is_checkmate(move_string):
    pass