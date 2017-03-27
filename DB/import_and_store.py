import os
from pgnparser.pgn import GameIterator
import settings.settings as csettings
import storage.games as store

__author__ = 'elvijs'

LIMIT = 10000

if __name__ == "__main__":
    mongo = store.Mongo()
    count = 0
    for game in GameIterator(os.path.join(csettings.BASEDIR, 'DB/OTB-HQ.pgn')):
        mongo.store_game(game.to_dict())
        count += 1
        if count % 1000 == 0:
            print("{} games imported".format(count))
