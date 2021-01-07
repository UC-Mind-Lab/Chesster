"""Tyler Westland's attempt at a chess AI"""
import chess
from collections import defaultdict
import numpy as np
import random
random.seed()

from .base import BaseAI
from ..timer.base import BaseTimer


class TylerWestlandAI(BaseAI):
    """This AI's plan:
    Do a minimax with a depth of an arbitrary depth.

    """
    @staticmethod
    def make_random_legal_move(board:chess.Board) -> chess.Move:
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

    
    @staticmethod
    def piece_score(piece:chess.Piece) -> int:
        """Get the absolute value of the score of a piece.
        Parameters
        ----------
        piece: chess.Piece:
            The piece to evaluate

        Returns
        -------
        int
            The score of said piece
        """
        if piece.piece_type == chess.PAWN:
            return 10
        elif piece.piece_type == chess.KNIGHT:
            return 30
        elif piece.piece_type == chess.BISHOP:
            return 30
        elif piece.piece_type == chess.ROOK:
            return 50
        elif piece.piece_type == chess.QUEEN:
            return 90
        elif piece.piece_type == chess.KING:
            return 900
        

    def simple_board_score(self, board:chess.Board) -> int:
        """Scores a board based on the pieces on the board.
        Ones own pieces are worth points, and opponents pieces
        are worth negative points.
        Note this has no concept of context, so it's really just
        useful for determining how to remove pieces.

        Parameters
        ----------
        board: chess.Board
            The chess board to score.

        Returns
        -------
        int
            The score of the board.
        """
        score = 0
        for piece in board.piece_map().values():
            if piece.color == self.color:
                score += self.piece_score(piece)
            else:
                score -= self.piece_score(piece)
        return score


    def simple_score_move(self, board:chess.Board, move:chess.Move) -> int:
        """Scores a move based on the simple score of the resulting board.

        Parameters
        ----------
        board: chess.Board
            The chess board to score a move against.
        move: chess.Move
            The move score

        Returns
        -------
        int
            The score of the resulting board.
        """
        board.push(move)
        score = self.simple_board_score(board)
        board.pop()
        return score


    def simple_score_moves(self, board:chess.Board, moves) -> dict:
        """Return dict of simple scores to moves that achieve that.
        Parameters
        ----------
        board: chess.Board
            The chess board to score moves against.
        moves: Iterable
            Assumed to be an iterable of chess.Move objects.

        Returns
        -------
        dict
            int (a score) -> list(chess.Move)
        """
        scored_moves = defaultdict(list)
        for move in moves:
            score = self.simple_score_move(board, move)
            scored_moves[score].append(move)
        return scored_moves


    def best_simple_move(self, board:chess.Board) -> chess.Move:
        """Return the best (random) move through simple analysis

        Parameters
        ----------
        board: chess.Board
            The chessboard to analyze and make a move upon.

        Returns
        -------
        chess.Move
            Move to make.
        """
        # Calculate the best possible moves based on a simple
        # score of the boards.
        scored_moves = self.simple_score_moves(board, 
                board.legal_moves)
        max_score = max(scored_moves.keys())

        # Choose a random move with the highest possible score
        return random.choice(scored_moves[max_score])


    def minimax(self, board:chess.Board, depth=2):
        """Return the minimax move with an arbitrary depth.

        Parameters
        ----------
        board: chess.Board
            The chessboard to analyze and make a move upon.
        depth: int
            The depth of half-moves to go to.

        Returns
        -------
        int, chess.Move
            Score of the move, and move to make.
        """
        depth -= 1
        scores = list()
        for move in board.legal_moves:
            board.push(move)
            if depth <= 0:
                scores.append(
                        (move,
                            self.simple_board_score(board)))
            else:
                deeper_move, deeper_score = self.minimax(board, depth)
                if deeper_score is not None:
                    scores.append((move, deeper_score))
                else:
                    scores.append(
                            (move,
                                self.simple_board_score(board)))
            board.pop()
           
        if len(scores) == 0:
            return None, None
        else:
            if board.turn == self.color:
                return max(scores, key=lambda s: s[1])
            else:
                return min(scores, key=lambda s: s[1])


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
        # Save the color of ourself, so that we always know it.
        self.color = board.turn

        m = self.minimax(board, depth=3)

        # Make the move
        return m[0]

