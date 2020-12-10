"""An "AI" that takes in human input.
This is really just a wrapper around human input
"""
import chess

from .base import BaseAI


class Human(BaseAI):
    """Take in human input to select a legal move."""
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
        # Default to null move
        move = chess.Move.null()

        # Ask for user input until given move is valid
        while not bool(move):
            uci = input("Select move in UCI format: ")
            try:
                move = chess.Move.from_uci(uci)
                if not board.is_legal(move):
                    print("Illegal move, try again")
                    # Reset to null move
                    move = chess.Move.null()
            except ValueError:
                print("Incorrect UCI format, try again")

        # Return selected legal move
        return move

