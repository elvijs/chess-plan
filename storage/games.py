import re
from pymongo import MongoClient

__author__ = 'elvijs'


class Mongo:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['chessplan']
        self.games_coll = self.db.games

    def store_game(self, game_doc):
        self.games_coll.insert(game_doc)


def clean_games(limit=None):
    """
    Remove superfluous information from the moves array
    """
    client = Mongo()
    games = client.games_coll.find({}, {'moves': 1})
    for i, game in enumerate(games):
        new_moves = _get_clean_moves(game['moves'])
        client.games_coll.update({'_id': game['_id']}, {'$set': {'moves': new_moves}})
        if limit and i > limit:
            break
        if i % 1000 == 0:
            print("{} games cleaned".format(i))


def _get_clean_moves(dirty_moves: list) -> list:
    """
    Return a version of the game containing only the clean moves
    """
    clean_moves = []
    for i, move in enumerate(dirty_moves):
        if _is_dirty(move):
            pass
        else:
            clean_moves.append(move)

    return clean_moves


def _is_dirty(move: str) -> bool:
    """
    Get rid of "moves" like {Game 123}
    """
    result = re.search(r'({.*})|(\()|(\))|(\d\s?-\s?\d)', move)
    if result:
        return True
    return False

if __name__ == "__main__":
    print("cleaning the moves")
    clean_games()
