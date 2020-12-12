"""An "AI" that takes in human input.
This is really just a wrapper around human input
"""
import chess
import os
import sys

from .base import BaseAI
from ..timer.base import BaseTimer


class Human(BaseAI):
    """Take in human input to select a legal move."""
    def make_move(self, board:chess.Board, timer:BaseTimer) -> chess.Move:
        """Return a legal move as selected by a human.

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
        # Default to null move
        move = chess.Move.null()

        # open up sys.stdin manually since this module is used
        # in multi-threading. The multiprocessing module will
        # close the sys.stdin object within other processes.
        with os.fdopen(0) as sys.stdin:
            # Ask for user input until given move is valid
            while not bool(move):
                # Get user input
                uci = input("Select move in UCI format: ")
                # Attempt to parse out input
                try:
                    move = chess.Move.from_uci(uci)
                    if not board.is_legal(move):
                        print("Illegal move, try again.")
                        print(f"{timer.seconds_left} seconds left")
                        # Reset to null move
                        move = chess.Move.null()
                except ValueError:
                    print("Incorrect UCI format, try again")
                    print(f"{timer.seconds_left} seconds left")


        # Return selected legal move
        return move

