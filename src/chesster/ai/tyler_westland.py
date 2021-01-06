"""Tyler Westland's attempt at a chess AI"""
import chess
import random
random.seed()

from .base import BaseAI
from ..timer.base import BaseTimer


class TylerWestlandAI(BaseAI):
    """This AI's plan:
    Pick a random move.

    """
    def make_move(self, board:chess.Board, timer:BaseTimer) -> chess.Move:
        """Return a really well thought out move.

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

