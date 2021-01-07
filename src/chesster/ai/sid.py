"""An AI that chooses a random legal move"""
import chess
import random
random.seed()

from .base import BaseAI
from ..timer.base import BaseTimer


class Sid(BaseAI):
    """Chooses a random legal move"""
    def make_move(self, board:chess.Board, timer:BaseTimer) -> chess.Move:
        """Return a random legal move.

        Parameters
        ----------
        board: chess.Board
            The chessboard to analyze and make a move upon.
        timer: BaseTimer
            The timer associated with this AI for this game.

        Returns
        -------
        chess.Move
            Move to make.
        """
        return random.choice(list(board.legal_moves))

