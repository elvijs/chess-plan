import re
from pymongo import MongoClient

__author__ = 'elvijs'


class Mongo:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['chessplan']
        self.games_coll = self.db.games
        self.heatmap_requests_coll = self.db.heatmap_requests

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
        if not _is_dirty(move):
            clean_moves.append(_get_clean_move(move))

    return clean_moves


def _is_dirty(move: str) -> bool:
    """
    Get rid of "moves" like {Game 123}
    """
    result = re.search(r'({.*})|(\()|(\))|(\d\s?-\s?\d)', move)
    if result:
        return True
    return False


def _get_clean_move(move: str):
    """
    Remove exclamation marks and question marks and
    check if the rest of the move is sensible
    """
    return re.sub('[!\?\+-]', '', move)


if __name__ == "__main__":
    print("cleaning the moves")
    clean_games()
