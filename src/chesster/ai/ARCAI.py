"""An AI that chooses a random legal move"""
import chess
import random
random.seed()

import numpy as np

from .base import BaseAI
from ..timer.base import BaseTimer

class ARCAI(BaseAI):

    def __init__(self):
        # PiecePoints = [Pawn, Knight, Bishop, Rook, Queen]
        self.PiecePoints = {'pawn': 1, 'knight': 2, 'bishop': 3, 'rook': 4, 'queen': 5}

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

        # Tell me what color I am on the first turn (should always be BLK for now)
        if board.fullmove_number == 1:
            if board.turn:
                print("WHT")

            else:
                print("BLK")
                print(self.PiecePoints['rook'])
                # print(chess.Board(board.board_fen()))


        # Assign Point Values to all legal moves
        # Create list of Point Values for legal moves with same indices as the moves in the legal move list
        MovePoints = []
        moves = list(board.legal_moves)
        for move in board.legal_moves:
            MovePoints.append(self.evalCurMove(move, board))

        return list(board.legal_moves)[np.argmax(MovePoints)]

    def evalCurMove(self, Move, board):
        # Base Point Value
        BasePoints = 0

        # Add Points
        CapturePoints = 1
        ReadyToCapturePoints = 0.5
        ForkPoints = 1
        CheckmatePoints = 10
        CheckPoints = 1.25
        PromotionPoints = 4

        Points = BasePoints

        if board.is_capture(Move):
            Points += CapturePoints
        if board.gives_check(Move):
            Points += CheckPoints
        if '#' in chess.Move.uci(Move):
            Points += CheckmatePoints
        if Move.promotion:
            Points += PromotionPoints

        # Push the move to check for points
        board.push(Move)
        # Check Number of Attacks a piece has if move is made, if >= 2, give points
        NumAttacks = 0

        for spot in list(board.attacks(Move.to_square)):
            if (board.color_at(spot) != board.turn) & (board.color_at(spot) is not None):
                NumAttacks += 1

        if NumAttacks >= 2:
            Points += ForkPoints
        elif NumAttacks == 1:
            Points += ReadyToCapturePoints

        NotLostPoint = [True, True, True]

        for move in board.legal_moves:
            Points += self.evalFutMove(move, board, NotLostPoint)[0]
            NotLostPoint = self.evalFutMove(move, board, NotLostPoint)[1]

        # pop the move back out so nobody gets confused
        board.pop()

        return Points

    def evalFutMove(self, Move, board, NotLostPoint):
        # Lose Points
        SuicidePoints = -1
        OpensCheckPoints = -0.5
        OpensCheckmatePoints = -10
        pointmod = 0

        if board.is_capture(Move) & NotLostPoint[0]:
            pointmod += SuicidePoints
            NotLostPoint[0] = False
        if board.gives_check(Move) & NotLostPoint[1]:
            pointmod += OpensCheckPoints
            NotLostPoint[1] = False
        if ('#' in chess.Move.uci(Move)) & NotLostPoint[2]:
            pointmod += OpensCheckmatePoints
            NotLostPoint[2] = False

        return pointmod, NotLostPoint
