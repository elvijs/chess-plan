import os
from lib.pgnparser.pgn import GameIterator
import settings.settings as csettings
import storage.storage as store

__author__ = 'elvijs'


mongo = store.Mongo()
count = 0
for game in GameIterator(os.path.join(csettings.BASEDIR, 'DB/OTB-HQ/test games.pgn')):
    mongo.store_game(game.to_dict())
    count += 1
    print(game)
    print(game.moves)
