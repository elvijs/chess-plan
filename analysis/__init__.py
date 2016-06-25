import logging

__author__ = 'elvijs'

logger = logging.getLogger("Move parser")

PIECES = {"p", "n", "b", "r", "q", "k"}
PIECE_IDENTIFIERS = {
    "pa2", "pb2", "pc2", "pd2", "pe2", "pf2", "pg2", "ph2",
    "pa7", "pb7", "pc7", "pd7", "pe7", "pf7", "pg7", "ph7",
    "ra1", "nb1", "bc1", "qd1", "ke1", "bf1", "ng1", "rh1",
    "ra8", "nb8", "bc8", "qd8", "ke8", "bf8", "ng8", "rh8"
}
SQUARE_LETTERS = {"a", "b", "c", "d", "e", "f", "g", "h"}
SQUARE_NUMBERS = {"1", "2", "3", "4", "5", "6", "7", "8"}
NON_PRAWNS = {"N", "B", "R", "Q", "K"}
CASTLE_MOVES = ["O-O", "O-O-O", "O-O+", "O-O-O+"]
ALLOWED_COLOURS = {"b", "w"}
