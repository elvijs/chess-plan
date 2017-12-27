__author__ = 'elvijs'

import time
import settings
from analysis.heatmaps import get_landing_heatmap_in_parallel
from analysis.compute import get_landing_heatmap, get_landing_heatmap_in_parallel


def time_fn(function, *args, **kwargs):
    st = time.time()
    function(*args, **kwargs)
    et = time.time()
    print("{0} took {1} seconds".format(function, et - st))


if __name__ == "__main__":
    alekhine_regex = '^B0[2-5].*'
    # time_fn(get_landing_heatmap_in_parallel, alekhine_regex)
    # time_fn(get_landing_heatmap, alekhine_regex)
