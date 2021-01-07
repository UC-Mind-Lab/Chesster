"""An AI that chooses a random legal move"""
import chess
import random
random.seed()

from .base import BaseAI
from ..timer.base import BaseTimer


class SteinsGate(BaseAI):
    """Chooses a random legal move"""
    def make_move(self, board: chess.Board, timer: BaseTimer) -> chess.Move:
        legal_moves = board.legal_moves
        move_value = 0
        move_found = False
        best_move_list = []
        """Iterate through all the legal moves and evaluate them for viability"""
        for move in legal_moves:
            value = self.get_move_value(board, move)
            """If the current move's value is better than the last move then make it the new best move"""
            if value > move_value:
                best_move_list = [move]     # Reset the list of possible best moves
                move_found = True
                move_value = value
            elif value == move_value:   # If the current move is equivalent to the last found best move, add it to the list of possible moves for selection
                best_move_list.append(move)
        if move_found:
            return random.choice(best_move_list)
        else:
            return random.choice(list(board.legal_moves))

    """Method that begins the process for evaluating how good a move is"""
    def get_move_value(self, board, move) -> int:
        value = 0
        if board.is_capture(move):
            value += self.get_piece_offset(board, move.to_square)
        if board.gives_check(move):
            value += 1
        value += self.danger_calculation(board, not board.turn, move.from_square)

        value += self.move_test(board, move)
        return value

    """Method that will generate an offset based on the values used by AlphaZero to rank pieces"""
    def get_piece_offset(self, board, square) -> int:
        offset = 0
        if board.piece_type_at(square) == 1:
            offset = 1
        elif board.piece_type_at(square) == 2:
            offset = 3.05
        elif board.piece_type_at(square) == 3:
            offset = 3.33
        elif board.piece_type_at(square) == 4:
            offset = 5.63
        elif board.piece_type_at(square) == 5:
            offset = 9.5
        return offset

    """Method for caluclating how much danger a piece is currently in or will be"""
    def danger_calculation(self, board, player_color, square) -> int:
        # print("Calculating danger coefficient")
        offset = 0
        attacker_squares = board.attackers(color=player_color, square=square)
        for attacker in attacker_squares:
            if board.piece_at(attacker) is not None:
                """These are different ways of weighting the danger a piece is currently in"""
                # offset += 1    # Weight by number of attackers
                offset += self.get_piece_offset(board, square)  # Weight by the piece value that is being attacked
                # offset += self.get_piece_offset(board, attacker)  # Weight by the piece value that is being attacked
                # print("Piece in danger!", chess.square_name(attacker), "attacking:", chess.square_name(square), offset)
        return offset

    """Method for testing a move and determining if it is a move for checkmate or if by moving it will be in danger"""
    def move_test(self, board, move) -> int:
        offset = 0
        board.push(move)
        """If the move is a checkmate, guarantee that it will be selected"""
        if board.turn:
            if board.is_checkmate():
                # print("Checkmate move found against WHITE!")
                offset += 100
                board.pop()
                return offset
        else:
            if board.is_checkmate():
                # print("Checkmate move found against BLACK!")
                offset += 100
                board.pop()
                return offset
        """Check if the move will threaten other pieces"""
        attacking_squares = board.attacks(square=move.to_square)
        for square in attacking_squares:
            if board.piece_at(square) is not None:
                if board.color_at(square) == board.turn:
                    """These are different ways of weighting the pieces that are being threatened by the potential move"""
                    # offset += self.get_piece_offset(board, square)    # Weight by piece value
                    # offset += (self.get_piece_offset(board, square) / 2)    # Weight by piece value / 2
                    # offset += board.piece_type_at(square) # Weight by the piece game ID
                    # offset += (board.piece_type_at(square) / 2)    # Weight by the piece game ID/2
                    offset += 1 # Weight by the number of pieces threatened
                    # print("Piece threatening!", chess.square_name(move.to_square), "attacking:", chess.square_name(square), offset)
        """Check if the move will put the current piece in danger"""
        offset -= self.danger_calculation(board, board.turn, move.to_square)
        board.pop()
        return offset
