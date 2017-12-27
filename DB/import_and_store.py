import os
import settings
from lib.pgnparser.pgn import GameIterator
import storage.games as store

__author__ = 'elvijs'

if __name__ == "__main__":
    mongo = store.Mongo()
    count = 0
    for game in GameIterator(os.path.join(settings.BASEDIR, 'DB/OTB-HQ.pgn')):
        mongo.store_game(game.to_dict())
        count += 1
        if count % 1000 == 0:
            print("{} games imported".format(count))
