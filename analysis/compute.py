"""
The computation module.
* Performs game queries and transports them from DB,
* Splits the games up for batch processing,
* Executes batches and merges the results together.
"""

import multiprocessing
import time

import analysis
from analysis.heatmaps import logger, NUM_CPUS_TO_USE, store, LandingHeatmap, LapseHeatmap


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
    partitioned_games = _get_partitioned_cursor(games, batchsize)
    t2 = time.time()
    pool = multiprocessing.Pool(processes=NUM_CPUS_TO_USE,)

    partial_heatmaps = pool.map(produce_landing_heatmap_dirty_version, partitioned_games)
    heatmap = LandingHeatmap()
    for partial_heatmap in partial_heatmaps:
        heatmap.update_with_another_heatmap(partial_heatmap)
    t3 = time.time()
    logger.info("heatmap produced in {0}s. Game lookup and partitioning took {1}s; "
                "heatmaps were computed in {2}s".format(t3-t1, t2-t1, t3-t2))
    return heatmap


def get_lapse_heatmap_in_parallel(regex, batchsize=1000):
    """
    1. Build a pool of :NUM_CPUS_TO_USE: processes.
    2. Partition the games into the same number of chunks.
    3. Produce heatmaps for each of the partitions in parallel.
    4. Reduce the partition heatmaps to a single master heatmap.
    """
    logger.info("computing the heatmap in parallel")
    t1 = time.time()
    games = get_games({'eco': {'$regex': regex}})
    partitioned_games = _get_partitioned_cursor(games, batchsize)
    t2 = time.time()
    pool = multiprocessing.Pool(processes=NUM_CPUS_TO_USE,)

    partial_heatmaps = pool.map(produce_lapse_heatmap_dirty_version, partitioned_games)
    heatmap = LapseHeatmap()
    for partial_heatmap in partial_heatmaps:
        heatmap.update_with_another_heatmap(partial_heatmap)
    t3 = time.time()
    logger.info("heatmap produced in {0}s. Game lookup and partitioning took {1}s; "
                "heatmaps were computed in {2}s".format(t3-t1, t2-t1, t3-t2))
    return heatmap


def _get_partitioned_cursor(cursor, batchsize):
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
    res = LandingHeatmap()

    count = 0
    for g in games:
        res.update_with_a_game(g, from_move, to_move)

        count += 1
        if count % 100 == 0:
            logger.debug("{} games processed".format(count))

    return res


def produce_landing_heatmap_dirty_version(games):
    """
    The same as produce_landing_heatmap(), but takes from_move and to_move parameters from
    analysis.__init__.py.
    This is disgusting, but necessary as the multiprocessing module doesn't accept
    passing arguments in functions.
    """
    logger.debug("processing a batch of {} games".format(len(games)))
    res = LandingHeatmap()

    count = 0
    for g in games:
        res.update_with_a_game(g, analysis.from_move, analysis.to_move)

        count += 1
        if count % 100 == 0:
            logger.debug("{} games processed".format(count))

    return res


def produce_lapse_heatmap_dirty_version(games):
    """
    Produce a lapse heatmap.
    Take from_move and to_move parameters from analysis.__init__.py.
    This is disgusting, but necessary as the multiprocessing module doesn't accept
    passing arguments in functions.
    """
    logger.debug("processing a batch of {} games".format(len(games)))
    res = LapseHeatmap()

    count = 0
    for g in games:
        res.update_with_a_game(g, analysis.from_move, analysis.to_move)

        count += 1
        if count % 100 == 0:
            logger.debug("{} games processed".format(count))

    return res
