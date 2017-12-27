import copy
import logging
import chess  # TODO: include in requirements.txt

import analysis
from analysis.parse import get_move_landing_squares

logger = logging.getLogger("Heatmaps")

__author__ = 'elvijs'

SQUARE_TO_NUMBER_MAP = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
HEATMAP_SQUARE_KEYS = {"p", "n", "b", "r", "q", "k", "all"}


class Heatmap:
    """
    A base class for all heatmaps.
    Consumes games and supports addition.
    """
    def __init__(self):
        self.state = self._get_starting_heatmap()

    def __add__(self, other):
        new_heatmap = copy.deepcopy(Heatmap)
        new_heatmap.update_with_another_heatmap(other)
        return new_heatmap

    def update_with_a_game(self, game, from_move, to_move):
        """
        Update the heatmap with the information from the provided game object.

        :param game: a dict() object that contains a 'moves' attribute.
        :param from_move: From which move to start updating the heatmap.
        :param to_move: At which move stop updating the heatmap.
        """
        game_heatmap = type(self)()  # this will be called from subclasses,
        # so need to ensure the right instance created
        game_heatmap.state = self._compute_game_heatmap_state(game, from_move, to_move)
        try:
            self.update_with_another_heatmap(game_heatmap)
        except Exception as ex:
            logger.exception(ex)
            logger.error("happened on the following game: {}".format(game))

    def _compute_game_heatmap_state(self, game, from_move, to_move):
        """
        Implement in subclasses.

        :param game: an instance of a Game.
        :param from_move: from which move to start updating the heatmap.
        :param to_move: at which move stop updating the heatmap.
        """
        raise Exception("implement in subclasses")

    def update_with_another_heatmap(self, heatmap):
        """
        Update this heatmap with information from the heatmap passed in.
        :param heatmap: a heatmap to be incorporated.
        :type heatmap: Heatmap
        """
        for i in range(0, len(self.state), 1):
            for k in HEATMAP_SQUARE_KEYS:
                for c in analysis.ALLOWED_COLOURS:
                    self.state[i][k][c] += heatmap.state[i][k][c]

    def _get_starting_heatmap(self):
        """
        Return the initial state for a heatmap.
        """
        ret = []
        for i in range(64):
            ret.append(self._get_basic_square_block())
        return ret

    @staticmethod
    def _get_basic_square_block():
        return dict(
            p=dict(w=0, b=0),
            n=dict(w=0, b=0),
            b=dict(w=0, b=0),
            r=dict(w=0, b=0),
            q=dict(w=0, b=0),
            k=dict(w=0, b=0),
            all=dict(w=0, b=0)
        )


class LandingHeatmap(Heatmap):
    """
    A heatmap of pieces landing on squares (as opposed to computing the lapse time on a square).
    """
    def _compute_game_heatmap_state(self, game, from_move, to_move):
        """
        Computes the landing heatmap for the provided game.
        If an exception is encountered, return an empty heatmap.

        :param game: a dict() object that contains a 'moves' attribute.
        :param from_move: optional. From which move to start updating the heatmap.
        :param to_move: optional. At which move stop updating the heatmap.
        """
        ret = self._get_starting_heatmap()
        moves = game['moves']
        current_colour = "w"
        upper_limit = min(to_move * 2, len(moves) - 1)
        lower_limit = min(from_move * 2, len(moves) - 1)
        for i in range(lower_limit, upper_limit, 1):
            try:
                move_tuples = get_move_landing_squares(moves[i], current_colour)
                for (piece, target_square) in move_tuples:
                    if (piece, target_square) == (None, None):
                        logger.debug("move parsing error, continuing")
                        continue
                    target_square_index = _convert_square_to_index(target_square)
                    ret[target_square_index][piece][current_colour] += 1
                    ret[target_square_index]["all"][current_colour] += 1

                current_colour = "b" if current_colour == "w" else "w"
            except Exception as ex:
                logger.info("exception whilst updating results with move string: {}".format(moves[i]))
                logger.exception(ex)
                return self._get_starting_heatmap()
        return ret


class LapseHeatmap(Heatmap):
    """
    A heatmap of piece lapse time on squares.
    """
    def _compute_game_heatmap_state(self, game, from_move, to_move):
        """
        Computes the lapse heatmap for the provided game.
        If an exception is encountered, return an empty heatmap.

        :param game: a dict() object that contains a 'moves' attribute.
        :param from_move: optional. From which move to start updating the heatmap.
        :param to_move: optional. At which move stop updating the heatmap.
        """
        heatmap_state = self._get_starting_heatmap()
        moves = game['moves']
        upper_limit = min(to_move * 2, len(moves) - 1)
        lower_limit = min(from_move * 2, len(moves) - 1)
        board = chess.Board()
        try:
            for i in range(0, upper_limit, 1):
                board.push_san(moves[i])
                if lower_limit <= i:
                    self._update_state_with_board(heatmap_state, board)
        except Exception as ex:
            logger.info("exception whilst updating results with move string: {}".format(moves[i]))
            logger.exception(ex)
            logger.info("board: \n")
            logger.info(board.__str__())
            return self._get_starting_heatmap()
        return heatmap_state

    @staticmethod
    def _update_state_with_board(state, board):
        """
        Update self.state with the current board information.

        TODO: move to the chess module formalism.
        :param board: the current board.
        :type board: chess.Board
        """
        for i, square in enumerate(chess.SQUARES_180):
            piece = board.piece_at(square)
            if piece:
                symbol = piece.symbol().lower()
                colour = _convert_color_to_string(piece.color)
                state[i][symbol][colour] += 1
                state[i]['all'][colour] += 1


def _convert_color_to_string(color):
    """
    Converts the chess module's color to "b" and "w".
    :param color:
    :return:
    """
    if color:
        return "w"
    else:
        return "b"


def _convert_square_to_index(target_square_string):
    """
    a8 --> 0
    h1 --> 63

    Corresponds to the squares as described in chess.SQUARES_180.

    :param target_square_string: a move in the algebraic chess notation
    :return: an index representing the sought square
    :rtype: int
    """
    letter = target_square_string[0]
    number = int(target_square_string[1])
    return ((8 - number) * 8) + SQUARE_TO_NUMBER_MAP[letter]
