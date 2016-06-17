from analysis.parse import get_move_landing_squares

__author__ = 'elvijs'


def test_parse_move():
    assert get_move_landing_squares("d4", "w") == [("p", "d4")]
    assert get_move_landing_squares("Nxa8", "b") == [("n", "a8")]
    assert get_move_landing_squares("O-O", "w") == [("k", "g1"), ("r", "f1")]
    assert get_move_landing_squares("invalid move", "b") == [(None, None)]
