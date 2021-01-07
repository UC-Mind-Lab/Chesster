"""Aaron's Top Notch AI that totally won't lose first round of the tournament"""
import chess
import random
random.seed()

import numpy as np

from .base import BaseAI
from ..timer.base import BaseTimer

class ARCAI(BaseAI):

    def __init__(self):
        # Base Point Value
        self.BasePoints = 0

        # Add Points
        self.CapturePoints = 1.5
        self.ReadyToCapturePoints = 0.5
        self.ForkPoints = 2
        self.CheckmatePoints = 10
        self.CheckPoints = 1
        self.PromotionPoints = 2
        self.run_it_down_pts = 1
        self.run_from_danger = 2

        # Lose Points
        self.RepeatPoints = -2
        self.SuicidePoints = -5
        self.OpensCheckPoints = -2
        self.OpensCheckmatePoints = -10

        # PiecePoints = [Pawn, Knight, Bishop, Rook, Queen, King?]
        self.PiecePoints = {1: 1, 2: 2, 3: 3, 4: 4, 5: 6, 6: 10}

    """Choose a move"""
    def make_move(self, board:chess.Board, timer:BaseTimer) -> chess.Move:
        """
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

        try:
            # My Last Move
            myPast = [board.move_stack[-2].from_square, board.move_stack[-2].to_square]
        except IndexError:
            # Handle First Turn Shenanigans
            myPast = [0, 0]

        try:
            # Opponents Last Move
            OppPast = [board.move_stack[-1].from_square, board.move_stack[-1].to_square]
        except IndexError:
            # Handle First Turn Shenanigans
            OppPast = [0, 0]

        x1 = np.copy(list(board.legal_moves))

        # Assign Point Values to all legal moves
        # Create list of Point Values for legal moves with same indices as the moves in the legal move list
        MovePoints = []
        for move in board.legal_moves:
            MovePoints.append(self.evalMoves(move, board, myPast, OppPast))

        try:
            return list(board.legal_moves)[np.argmax(MovePoints)]
        except IndexError:
            return random.choice(list(x1))

    # Evaluate them moves brother
    def evalMoves(self, move, board, myPast, OppPast):
        my_pts = 0
        if move in board.legal_moves:
            # Add My Points
            mycolor = board.turn
            othercolor = not mycolor
            oppPieceNum = 0
            for i in board.piece_map().values():
                if i.color == othercolor:
                    oppPieceNum += 1
                if (i.color == mycolor) & (i.piece_type == 5):
                        if len(board.attackers(board.turn, move.to_square)) < \
                                len(board.attackers(board.turn, move.from_square)):
                            my_pts += 2.5
                            if len(board.attackers(board.turn, move.to_square)) < 1:
                                my_pts += 2.5

            if oppPieceNum <= 3:
                if chess.square_distance(move.to_square, board.king(othercolor)) < \
                        chess.square_distance(move.from_square, board.king(othercolor)):
                    my_pts += self.run_it_down_pts

            if board.is_capture(move):
                # Base Capture Point Addition
                my_pts += self.CapturePoints
                # Additional Bonus based on piece type
                try:
                    my_pts += self.PiecePoints[board.piece_at(move.to_square).piece_type]
                    # print("bonus of", self.PiecePoints[board.piece_at(move.to_square).piece_type])
                except KeyError:
                    my_pts += 0
                except AttributeError:
                    my_pts += 0
            if move in board.legal_moves:
                if board.gives_check(move):
                    my_pts += self.CheckPoints
                    if board.is_checkmate():
                        my_pts += self.CheckmatePoints
                        return my_pts
            if move.promotion:
                my_pts += self.PromotionPoints
            if (move.from_square == myPast[1]) & (move.to_square == myPast[0]):
                my_pts += self.RepeatPoints

            if len(board.attackers(board.turn, move.to_square)) < len(board.attackers(board.turn, move.from_square)):
                my_pts += self.run_from_danger


            # Make My Move
            nb1 = board
            nb1.push(move)

            if nb1.is_checkmate():
                my_pts += self.CheckmatePoints
                return my_pts
            # Subtract From My Points and Add Attack Bonuses
            # Add Attack Bonuses
            NumAttacks = 0

            for spot in list(nb1.attacks(move.to_square)):
                if (nb1.color_at(spot) != nb1.turn) & (nb1.color_at(spot) is not None):
                    NumAttacks += 1
            if NumAttacks >= 2:
                my_pts += self.ForkPoints
            elif NumAttacks == 1:
                my_pts += self.ReadyToCapturePoints

            # Subtract From My Points
            all_opp_pts = []
            NotLostPoint = [True, True, True]
            for opp_move in nb1.legal_moves:
                point_mod = 0
                opp_pts = self.BasePoints
                if (nb1.is_capture(opp_move)) & (NotLostPoint[0]):
                    point_mod += self.SuicidePoints
                    NotLostPoint[0] = False
                if (nb1.gives_check(opp_move)) & (NotLostPoint[1]):
                    point_mod += self.OpensCheckPoints
                    NotLostPoint[1] = False
                my_pts += point_mod

                # Add Opponents Move Points
                if nb1.is_capture(opp_move):
                    # Base Capture Point Addition
                    opp_pts += self.CapturePoints
                    # Additional Bonus based on piece type
                    try:
                        opp_pts += self.PiecePoints[nb1.piece_at(opp_move.to_square).piece_type]
                    except KeyError:
                        opp_pts += 0
                    except AttributeError:
                        opp_pts += 0
                if nb1.gives_check(opp_move):
                    opp_pts += self.CheckPoints
                if opp_move.promotion:
                    opp_pts += self.PromotionPoints
                if (opp_move.from_square == OppPast[1]) & (opp_move.to_square == OppPast[0]):
                    opp_pts += self.RepeatPoints

                # Makes Opponents Moves
                nb1.push(opp_move)

                # Subtract From Opponent Points and Add Attack Bonuses
                # Add Attack Bonuses
                NumAttacks = 0

                for spot in list(nb1.attacks(opp_move.to_square)):
                    if (nb1.color_at(spot) != nb1.turn) & (nb1.color_at(spot) is not None):
                        NumAttacks += 1
                if NumAttacks >= 2:
                    opp_pts += self.ForkPoints
                elif NumAttacks == 1:
                    opp_pts += self.ReadyToCapturePoints

                # Subtract From Opponent Points
                NotLostPoint = [True, True, True]
                for next_move in nb1.legal_moves:
                    point_mod = 0
                    if (nb1.is_capture(next_move)) & (NotLostPoint[0]):
                        point_mod += self.SuicidePoints
                        NotLostPoint[0] = False
                    if (nb1.gives_check(next_move)) & (NotLostPoint[1]):
                        point_mod += self.OpensCheckPoints
                        NotLostPoint[1] = False
                    opp_pts += point_mod

                # POP OPPONENT MOVE
                nb1.pop()

                all_opp_pts.append(opp_pts)

            # Find and Make Opponent's Optimal Move
            if len(list(nb1.legal_moves)) != 0:
                optimal_opp_move = list(nb1.legal_moves)[np.argmax(all_opp_pts)]
                nb1.push(optimal_opp_move)

                # GET POINTS FOR ALL MY NEXT MOVES
                for next_move in nb1.legal_moves:

                    # Add My Points
                    if nb1.is_capture(next_move):
                        # Base Capture Point Addition
                        my_pts += self.CapturePoints
                        # Additional Bonus based on piece type
                        try:
                            my_pts += self.PiecePoints[nb1.piece_at(next_move.to_square).piece_type]
                        except KeyError:
                            my_pts += 0
                        except AttributeError:
                            my_pts += 0
                    if nb1.gives_check(next_move):
                        my_pts += self.CheckPoints
                    if move.promotion:
                        my_pts += self.PromotionPoints
                    # I ignored repeat penalty because it sounds hard to make work rn

                    # MAKE MY NEXT MOVE
                    nb1.push(next_move)

                    # ADD ATTACK BONUSES
                    num_attacks = 0
                    for spot in list(nb1.attacks(next_move.to_square)):
                        if (nb1.color_at(spot) != nb1.turn) & (nb1.color_at(spot) is not None):
                            num_attacks += 1
                    if num_attacks >= 2:
                        my_pts += self.ForkPoints
                    elif num_attacks == 1:
                        my_pts += self.ReadyToCapturePoints

                    # SUBTRACT MY POINTS
                    NotLostPoint = [True, True, True]
                    for opp_next_move in nb1.legal_moves:
                        point_mod = 0
                        if (nb1.is_capture(opp_next_move)) & (NotLostPoint[0]):
                            point_mod += self.SuicidePoints
                            NotLostPoint[0] = False
                        if (nb1.gives_check(opp_next_move)) & (NotLostPoint[1]):
                            point_mod += self.OpensCheckPoints
                            NotLostPoint[1] = False
                        my_pts += point_mod

                    # POP MY NEXT MOVE
                    nb1.pop()

                # POP OPPONENT MOVE
                nb1.pop()

            # POP MY MOVE
            nb1.pop()


            return my_pts

        # print(chess.Board(board.fen()))
        return my_pts
