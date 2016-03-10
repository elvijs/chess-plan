from analysis.parse import MoveIsCastle, parse_move
from storage.storage import Mongo

__author__ = 'elvijs'

store = Mongo()

SQUARE_TO_NUMBER_MAP = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}


def get_projects_from_eco(eco_code):
    return store.games_coll.find({'eco': eco_code})


def produce_heatmap(projects, piece_colour):
    """
    Returns an array [d1, d2, ... d64], where each of the dicts represents
    a square in the following order: (a8, b8, c8 ... ,f1, g1, h1).
    Each of the dicts should look like:
    {
      "p": {"w": 10474, "b": 0},
      "n": {"w": 15363, "b": 14358},
      "b": {...},
      "r": {...},
      "q": {...},
      "k": {...},
      "all": {...}
    }
    """
    res = _get_init_heatmap()

    for p in projects:
        _update_results_arr_with_landing_info(p, res, piece_colour)

    return res


def _update_results_arr_with_landing_info(project, partial_results_dict, piece_colour):
    moves = project['moves']
    if piece_colour == "w":
        move_offset = 0
    else:
        move_offset = 1

    for i in range(move_offset, len(moves), 2):  # note that this (correctly) omits the last "result move"
        try:
            piece, target_square = parse_move(moves[i])
            target_square_index = _convert_square_to_index(target_square)
            partial_results_dict[target_square_index][piece][piece_colour] += 1
            partial_results_dict[target_square_index]["all"][piece_colour] += 1
        except MoveIsCastle as ex:
            print(ex)


def _convert_square_to_index(target_square_string):
    letter = target_square_string[0]
    number = int(target_square_string[1])
    return ((8 - number) * 8) + SQUARE_TO_NUMBER_MAP[letter]


def _get_init_heatmap():
    ret = []
    for i in range(64):
        ret.append(_get_basic_square_block())
    return ret


def _get_basic_square_block():
    return dict(
        p=dict(w=0, b=0),
        n=dict(w=0, b=0),
        b=dict(w=0, b=0),
        r=dict(w=0, b=0),
        q=dict(w=0, b=0),
        k=dict(w=0, b=0),
        all=dict(w=0, b=0)
    )
