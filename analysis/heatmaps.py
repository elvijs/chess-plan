from analysis.parse import get_move_landing_squares
from storage.storage import Mongo
import logging

logger = logging.getLogger("Heatmaps")

__author__ = 'elvijs'

store = Mongo()

SQUARE_TO_NUMBER_MAP = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}


def get_processed_heatmap_data(regex):
    logger.info("request sent")
    games = get_games({'eco': {'$regex': regex}})
    ret = produce_heatmap(games, update_results_with_landing_info)

    return ret


def get_games(query):
    return store.games_coll.find(query)


def produce_heatmap(games, results_update_method):
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
    :piece_colour: - "w" or "b"
    """
    logger.info("{} games found".format(games.count()))
    res = _get_init_heatmap()

    count = 0
    for g in games:
        try:
            results_update_method(g, res)
        except Exception as ex:
            logger.exception(ex)
            logger.error("happened on the following game:")
            logger.error(g)

        count += 1

        if count % 100 == 0:
            logger.info("{} games processed".format(count))

    return res


def update_results_with_landing_info(game, partial_results_dict):
    moves = game['moves']
    current_colour = "w"
    for i in range(0, len(moves) - 1, 1):  # note that this (correctly) omits the last "result move"
        try:
            move_tuples = get_move_landing_squares(moves[i], current_colour)
            for (piece, target_square) in move_tuples:
                if (piece, target_square) == (None, None):
                    logger.info("move parsing error, continuing")
                    continue
                target_square_index = _convert_square_to_index(target_square)
                partial_results_dict[target_square_index][piece][current_colour] += 1
                partial_results_dict[target_square_index]["all"][current_colour] += 1

            current_colour = "b" if current_colour == "w" else "w"
        except Exception as ex:
            logger.info("exception whilst updating results with move string: {}".format(moves[i]))
            logger.exception(ex)


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
