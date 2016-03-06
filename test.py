import os
from lib.pgnparser.pgn import GameIterator
import settings

__author__ = 'elvijs'

for game in GameIterator(os.path.join(settings.BASEDIR, 'DB/OTB-HQ/test games.pgn')):
    print(game)
    print(game.moves)
