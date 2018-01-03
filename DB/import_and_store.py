"""
A simple script to read a PGN file and store the games in the Mongo DB.
"""

import os
import settings
from lib.pgnparser.pgn import GameIterator
from storage.games import Mongo

__author__ = 'elvijs'

PGN_PATH = 'DB/all_games.pgn'
ENCODING = 'iso-8859-1'  # get via `file -i $PGN_PATH`


if __name__ == "__main__":
    mongo_client = Mongo()
    count = 0
    for game in GameIterator(os.path.join(settings.BASEDIR, PGN_PATH), encoding='iso-8859-1'):
        mongo_client.store_game(game.to_dict())
        count += 1
        if count % 1000 == 0:
            print("{} games imported".format(count))

    print("In total {} games imported".format(count))
