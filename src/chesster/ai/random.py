"""An AI that chooses a random legal move"""
import chess
import random
random.seed()

from .base import BaseAI


class RandomAI(BaseAI):
    """Chooses a random legal move"""
    def make_move(self, board:chess.Board) -> chess.Move:
        """Return a random legal move.

        Parameters
        ----------
        board: chess.Board
            The chessboard to analyze and make a move upon.

        Returns
        -------
        chess.Move
            Move to make.
        """
        return random.choice(list(board.legal_moves))

