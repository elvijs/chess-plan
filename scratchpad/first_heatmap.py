__author__ = 'elvijs'

from analysis.heatmaps import produce_heatmap, get_games, update_results_with_landing_info

alekhine_games = get_games({'eco': {'$regex': 'B0[2-5].*'}})
print("found {} Alekhine's defence games".format(alekhine_games.count()))

hm = produce_heatmap(alekhine_games, "w", update_results_with_landing_info)
import pprint
pprint.pprint(hm)
