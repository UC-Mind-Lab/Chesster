"""The base AI object that defines the API for AI in Chesster"""
import abc
import chess

from ..timer.base import BaseTimer


class BaseAI(abc.ABC):
    """The API that AI's must conform to within Chesster"""

    @abc.abstractmethod
    def make_move(self, board:chess.Board, timer:BaseTimer) -> chess.Move:
        """Given the state of the board return the UCI notation move to make.

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
        ...

