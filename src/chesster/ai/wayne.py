"""An AI that chooses a random legal move"""
import chess
import math
import random
random.seed()

from .base import BaseAI
from ..timer.base import BaseTimer


class Wayne(BaseAI):
    # Maximum number of half moves (should be an even number, probably)
    MAX_DEPTH = 3
    # Values of the peices
    PIECE_VALS = {
        chess.PAWN: 1,
        chess.KNIGHT: 3.05,
        chess.BISHOP: 3.33,
        chess.ROOK: 5.63,
        chess.QUEEN: 9.5,
        chess.KING: 4,
    }

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
        self.color = board.turn
        mm = self.minimax(board, True, Wayne.MAX_DEPTH, -math.inf, math.inf)
        print(f'Score: {mm[1]}')
        return mm[0]
        # return random.choice(list(board.legal_moves))

    def eval_board(self, board:chess.Board) -> float:
        result = board.result(claim_draw = True)
        # Check for win
        if (result == '1-0' and self.color) or (result == '0-1' and not self.color):
            return math.inf
        # Check for loss
        if (result == '1-0' and not self.color) or (result == '0-1' and self.color):
            return -math.inf
        # Check for tie
        if (result == '1/2-1/2'):
            return 0 # Weight tie 0 for now, maybe check timer later?
        score = 0
        pieces = board.piece_map().values()
        for p in pieces:
            if (self.color == p.color):
                score += Wayne.PIECE_VALS[p.piece_type]
            else:
                score -= Wayne.PIECE_VALS[p.piece_type]
        return score

    def minimax(self, board:chess.Board, maxi:bool, depth:int, alpha:float, beta:float) -> tuple:
        if ((depth == 0) or board.is_game_over(claim_draw = True)):
            return (None, self.eval_board(board))
        legal_moves = list(board.legal_moves)
        best_move = str()
        best_score = -math.inf if maxi else math.inf
        for m in legal_moves:
            board.push(m)
            move, score = self.minimax(board, not maxi, depth - 1, alpha, beta)
            # Check new best move
            if (maxi and (score > best_score)) or ((not maxi) and (score < best_score)):
                best_move = m
                best_score = score
            board.pop()
            if maxi:
                if best_score >= beta:
                    return (best_move, best_score)
                if best_score > alpha:
                    alpha = best_score
            else:
                if best_score <= alpha:
                    return (best_move, best_score)
                if best_score < beta:
                    beta = best_score
        return (best_move, best_score)

