import logging
import analysis
import multiprocessing
import time
from storage.storage import Mongo
from analysis.parse import get_move_landing_squares

logger = logging.getLogger("Heatmaps")

__author__ = 'elvijs'

store = Mongo()

SQUARE_TO_NUMBER_MAP = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
HEATMAP_SQUARE_KEYS = {"p", "n", "b", "r", "q", "k", "all"}
NUM_CPUS_TO_USE = multiprocessing.cpu_count()


def get_landing_heatmap(regex):
    logger.info("request sent")
    t1 = time.time()
    games = list(get_games({'eco': {'$regex': regex}}))
    t2 = time.time()
    ret = produce_landing_heatmap(games)
    t3 = time.time()
    logger.info("heatmap produced in {0}s. Game lookup took {1}s; "
                "heatmaps were computed in {2}s".format(t3-t1, t2-t1, t3-t2))
    return ret


def get_landing_heatmap_in_parallel(regex, batchsize=1000):
    """
    1. Build a pool of :NUM_CPUS_TO_USE: processes.
    2. Partition the games into the same number of chunks.
    3. Produce heatmaps for each of the partitions in parallel.
    4. Reduce the partition heatmaps to a single master heatmap.
    """
    logger.info("computing the heatmap in parallel")
    t1 = time.time()
    games = get_games({'eco': {'$regex': regex}})
    partitioned_games = get_partitioned_cursor(games, batchsize)
    t2 = time.time()
    pool = multiprocessing.Pool(processes=NUM_CPUS_TO_USE,)

    partial_heatmaps = pool.map(produce_landing_heatmap_dirty_version, partitioned_games)
    ret = _get_starting_heatmap()
    for partial_heatmap in partial_heatmaps:
        merge_second_heatmap_into_first(ret, partial_heatmap)
    t3 = time.time()
    logger.info("heatmap produced in {0}s. Game lookup and partitioning took {1}s; "
                "heatmaps were computed in {2}s".format(t3-t1, t2-t1, t3-t2))
    return ret


def get_partitioned_cursor(cursor, batchsize):
    batch_count = 0
    batch = []
    for doc in cursor:
        batch_count += 1
        batch.append(doc)
        if batch_count >= batchsize:
            yield batch
            batch_count = 0
            batch = []
    yield batch


def get_games(query):
    return store.games_coll.find(query)


def produce_landing_heatmap(games, from_move=0, to_move=100):
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
    logger.debug("processing a batch of {} games".format(len(games)))
    res = _get_starting_heatmap()

    count = 0
    for g in games:
        try:
            game_heatmap = compute_game_landing_heatmap(g, from_move, to_move)
            merge_second_heatmap_into_first(res, game_heatmap)
        except Exception as ex:
            logger.exception(ex)
            logger.error("happened on the following game:")
            logger.error(g)

        count += 1

        if count % 100 == 0:
            logger.debug("{} games processed".format(count))

    return res


def produce_landing_heatmap_dirty_version(games):
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
    logger.debug("processing a batch of {} games".format(len(games)))
    res = _get_starting_heatmap()

    count = 0
    for g in games:
        try:
            game_heatmap = compute_game_landing_heatmap(g, analysis.from_move, analysis.to_move)
            merge_second_heatmap_into_first(res, game_heatmap)
        except Exception as ex:
            logger.exception(ex)
            logger.error("happened on the following game:")
            logger.error(g)

        count += 1

        if count % 100 == 0:
            logger.debug("{} games processed".format(count))

    return res


def compute_game_landing_heatmap(game, from_move, to_move):
    """
    Computes the landing heatmap for the provided game.
    If an exception is encountered, return an empty heatmap.
    """
    ret = _get_starting_heatmap()
    moves = game['moves']
    current_colour = "w"
    upper_limit = min(to_move*2, len(moves))
    for i in range(from_move, upper_limit, 1):
        try:
            move_tuples = get_move_landing_squares(moves[i], current_colour)
            for (piece, target_square) in move_tuples:
                if (piece, target_square) == (None, None):
                    logger.debug("move parsing error, continuing")
                    continue
                target_square_index = _convert_square_to_index(target_square)
                ret[target_square_index][piece][current_colour] += 1
                ret[target_square_index]["all"][current_colour] += 1

            current_colour = "b" if current_colour == "w" else "w"
        except Exception as ex:
            logger.info("exception whilst updating results with move string: {}".format(moves[i]))
            logger.exception(ex)
            return _get_starting_heatmap()
    return ret


def merge_second_heatmap_into_first(heatmap1, heatmap2):
    for i in range(0, len(heatmap1), 1):
        for k in HEATMAP_SQUARE_KEYS:
            for c in analysis.ALLOWED_COLOURS:
                heatmap1[i][k][c] += heatmap2[i][k][c]


def _convert_square_to_index(target_square_string):
    letter = target_square_string[0]
    number = int(target_square_string[1])
    return ((8 - number) * 8) + SQUARE_TO_NUMBER_MAP[letter]


def _get_starting_heatmap():
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
