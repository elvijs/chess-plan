__author__ = 'elvijs'


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
