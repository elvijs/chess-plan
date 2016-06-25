from analysis.parse import get_move_landing_squares, get_board, get_initial_board

__author__ = 'elvijs'


def test_parse_move():
    assert get_move_landing_squares("d4", "w") == [("p", "d4")]
    assert get_move_landing_squares("Nxa8", "b") == [("n", "a8")]
    assert get_move_landing_squares("O-O", "w") == [("k", "g1"), ("r", "f1")]
    assert get_move_landing_squares("invalid move", "b") == [(None, None)]


def test_board_update():
    move_descriptions = [
        {
            "piece_movements": [
                {
                    "piece": "pe2",
                    "from": "e2",
                    "to": "e4"
                },
                {
                    "piece": "pe7",
                    "from": "e7",
                    "to": "e5"
                }
            ]
        }
    ]
    board = get_board(move_descriptions)

    expected_board = get_initial_board()
    expected_board['e2'] = None
    expected_board['e7'] = None
    expected_board['e4'] = "pe2"
    expected_board['e5'] = "pe7"

    assert board == expected_board
