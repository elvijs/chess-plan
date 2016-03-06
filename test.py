import os
from lib.pgnparser.pgn import GameIterator
import settings
import storage

__author__ = 'elvijs'


mongo = storage.Mongo()
count = 0
for game in GameIterator(os.path.join(settings.BASEDIR, 'DB/OTB-HQ/test games.pgn')):
    mongo.store_game(game.to_dict())
    count += 1
    print(game)
    print(game.moves)
