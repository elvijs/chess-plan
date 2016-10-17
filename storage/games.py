from pymongo import MongoClient

__author__ = 'elvijs'


class Mongo:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['chessplan']
        self.games_coll = self.db.games

    def store_game(self, game_doc):
        self.games_coll.insert(game_doc)
