"""The base AI object that defines the API for AI in Chesster"""
import abc
import chess


class BaseAI(abc.ABC):
    """The API that AI's must conform to within Chesster"""

    @abc.abstractmethod
    def make_move(self, board:chess.Board) -> chess.Move:
        """Given the state of the board return the UCI notation move to make.

        Parameters
        ----------
        board: chess.Board
            The chessboard to analyze and make a move upon.

        Returns
        -------
        chess.Move
            Move to make.
        """
        ...

