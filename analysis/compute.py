"""
The computation module.
* Performs game queries and transports them from DB,
* Splits the games up for batch processing,
* Executes batches and merges the results together.
"""
import time
import multiprocessing

from storage.games import Mongo
from analysis.heatmaps import logger, LandingHeatmap, LapseHeatmap


class HeatmapManager:
    """
    A class to manage the computation of heatmaps including
    * successful computation storage
    * parallelisation
    """
    def __init__(self, num_processes=multiprocessing.cpu_count()):
        self._db_client = Mongo()
        self._pool = multiprocessing.Pool(processes=num_processes)

    def compute_landing_heatmap(self, regex: str, from_move: int, to_move: int,
                                batch_size: int=1000):
        """
        1. Partition the games into chunks of size :batch_size:.
        2. Produce heatmaps for each of the partitions in parallel.
        3. Reduce the partition heatmaps to a single master heatmap.
        """
        logger.info("computing the landing heatmap in parallel")
        t1 = time.time()
        games = self._get_games({'eco': {'$regex': regex}})
        params = dict(
            from_move=from_move,
            to_move=to_move,
        )
        partitioned_games = _get_partitioned_cursor(games, batch_size, params_to_inject=params)
        t2 = time.time()
        logger.info("game lookup and partitioning took {}s".format(t2 - t1))

        partial_heatmaps = self._pool.map(_produce_landing_heatmap, partitioned_games)
        heatmap = LandingHeatmap()
        for partial_heatmap in partial_heatmaps:
            heatmap.update_with_another_heatmap(partial_heatmap)
        t3 = time.time()
        logger.info("heatmaps were computed in {}s".format(t3 - t2))

        logger.info("total time taken: {}s".format(t3 - t1))
        return heatmap

    def compute_lapse_heatmap(self, regex: str, from_move: int, to_move: int,
                              batch_size: int = 1000):
        """
        1. Partition the games into chunks of size :batch_size:.
        2. Produce heatmaps for each of the partitions in parallel.
        3. Reduce the partition heatmaps to a single master heatmap.
        """
        logger.info("computing the lapse heatmap")
        t1 = time.time()
        games = self._get_games({'eco': {'$regex': regex}})
        params = dict(
            from_move=from_move,
            to_move=to_move,
        )
        partitioned_games = _get_partitioned_cursor(games, batch_size, params_to_inject=params)
        t2 = time.time()
        logger.info("game lookup and partitioning took {}s".format(t2 - t1))

        partial_heatmaps = self._pool.map(_produce_lapse_heatmap, partitioned_games)
        heatmap = LapseHeatmap()
        for partial_heatmap in partial_heatmaps:
            heatmap.update_with_another_heatmap(partial_heatmap)
        t3 = time.time()
        logger.info("heatmaps were computed in {}s".format(t3-t2))

        logger.info("total time taken: {}s".format(t3 - t1))
        return heatmap

    def _get_games(self, query):
        return self._db_client.games_coll.find(query)

    def _compute_and_store_landing_heatmap(self) -> None:
        """
        TODO: implement caching of computed heatmaps
        """
        pass


def _produce_landing_heatmap(games):
    """
    Compute the landing heatmap for the provided games that have
    from_move and to_move params injected in them.

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
    res = LandingHeatmap()

    count = 0
    for g in games:
        from_move = g['injected_params']['from_move']
        to_move = g['injected_params']['to_move']
        res.update_with_a_game(g, from_move, to_move)

        count += 1
        if count % 100 == 0:
            logger.debug("{} games processed".format(count))

    return res


def _produce_lapse_heatmap(games):
    """
    Compute the lapse heatmap for the provided games that have
    from_move and to_move params injected in them.

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
    res = LapseHeatmap()

    count = 0
    for g in games:
        from_move = g['injected_params']['from_move']
        to_move = g['injected_params']['to_move']
        res.update_with_a_game(g, from_move, to_move)

        count += 1
        if count % 100 == 0:
            logger.debug("{} games processed".format(count))

    return res


def _get_partitioned_cursor(cursor, batch_size: int, params_to_inject: dict=None):
    """
    Given a cursor:
    1. inject a params dict under 'injected_params' into each document
    2. batch the incoming documents into batch_size chunks and yield them on demand
    """
    batch_count = 0
    batch = []
    for doc in cursor:
        doc['injected_params'] = params_to_inject
        batch_count += 1
        batch.append(doc)
        if batch_count >= batch_size:
            yield batch
            batch_count = 0
            batch = []
    yield batch
