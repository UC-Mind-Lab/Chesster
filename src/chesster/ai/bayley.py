"""An AI that chooses a random legal move"""
import chess
import random
random.seed()

from .base import BaseAI
from ..timer.base import BaseTimer

'''
king_pos = [
    [-3.0,-4.0,-4.0,-5.0,-5.0,-4.0,-4.0,-3.0],
    [-3.0,-4.0,-4.0,-5.0,-5.0,-4.0,-4.0,-3.0],
    [-3.0,-4.0,-4.0,-5.0,-5.0,-4.0,-4.0,-3.0],
    [-3.0,-4.0,-4.0,-5.0,-5.0,-4.0,-4.0,-3.0],
    [-2.0,-3.0,-3.0,-4.0,-4.0,-3.0,-3.0,-2.0],
    [-1,0,-2.0,-2.0,-2.0,-2.0,-2.0,-2.0,-1.0],
    [ 2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
    [ 2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]
]
queen_pos = [
    [-2.0,-1.0,-1.0,-0.5,-0.5,-1.0,-1.0,-2.0],
    [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,-1.0],
    [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0,-1.0],
    [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0,-0.5],
    [ 0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0,-0.5],
    [-1,0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0,-1.0],
    [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0,-1.0],
    [-2.0,-1.0,-1.0,-0.5,-0.5,-1.0,-1.0,-2.0]
]
rook_pos = [
    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [ 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,-0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,-0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,-0.5],
    [-0,5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,-0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,-0.5],
    [ 0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]
]
bishop_pos = [
    [-2.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-2.0],
    [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,-1.0],
    [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0,-1.0],
    [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5,-1.0],
    [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0,-1.0],
    [-1,0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,-1.0],
    [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5,-1.0],
    [-2.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-2.0]
]
knight_pos = [
    [-5.0,-4.0,-3.0,-3.0,-3.0,-3.0,-4.0,-5.0],
    [-4.0,-2.0, 0.0, 0.0, 0.0, 0.0,-2.0,-4.0],
    [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0,-3.0],
    [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5,-3.0],
    [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0,-3.0],
    [-3,0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5,-3.0],
    [-4.0,-2.0, 0.0, 0.5, 0.5, 0.0,-2.0,-4.0],
    [-5.0,-4.0,-3.0,-3.0,-3.0,-3.0,-4.0,-5.0]
]
pawn_pos = [
    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [ 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
    [ 1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
    [ 0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
    [ 0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
    [ 0,5,-0.5,-1.0, 0.0, 0.0,-1.0,-0.5, 0.5],
    [ 0.5, 1.0, 1.0,-2.0,-2.0, 1.0, 1.0, 0.5],
    [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
]
'''

class BayleyAI(BaseAI):
    """Chooses a move from an alpha beta algorithm"""
    def make_move(self, board:chess.Board, timer:BaseTimer) -> chess.Move:
        """Return a move determined from alpha beta pruning.

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
        '''
        scores = []
        for move in board.legal_moves:
            scores.append(self.alphaBetaMax(-99999,99999,3,move,board))
        loc = scores.index(max(scores))
        return list(board.legal_moves)[loc]
        '''
        score,move = self.alphaBetaMax(-99999,99999,3,list(board.legal_moves)[0],board)
        return move


    def eval_move_shannon(
        self, move, 
        board:chess.Board
    ):
        """ Returns the score of a move using Shannon's algorithm

        f(p) = 200(K-K')
       + 9(Q-Q')
       + 5(R-R')
       + 3(B-B' + N-N')
       + 1(P-P')
       - 0.5(D-D' + S-S' + I-I')
       + 0.1(M-M') + ...

        KQRBNP = number of kings, queens, rooks, bishops, knights and pawns
        D,S,I = doubled, blocked and isolated pawns
        M = Mobility (the number of legal moves)

        lower case letters = black pieces
        upper case letters = white pieces
        """
        '''
        print('black')
        print(len(board.pieces(chess.KING,board.turn)))
        print(len(board.pieces(chess.QUEEN,0)))
        print(len(board.pieces(chess.ROOK,0)))
        print(len(board.pieces(chess.BISHOP,0)))
        print(len(board.pieces(chess.KNIGHT,0)))
        print(len(board.pieces(chess.PAWN,0)))
        print(len(board.pieces(chess.KING,0)))
        print('white')
        print(len(board.pieces(chess.KING,not board.turn)))
        print(len(board.pieces(chess.QUEEN,1)))
        print(len(board.pieces(chess.ROOK,1)))
        print(len(board.pieces(chess.BISHOP,1)))
        print(len(board.pieces(chess.KNIGHT,1)))
        print(len(board.pieces(chess.PAWN,1)))
        print(len(board.pieces(chess.KING,1)))
        '''

        temp_moves = len(list((board.legal_moves)))
        board.pop()
        score = 200 * (len(board.pieces(chess.KING,board.turn)) - len(board.pieces(chess.KING,not board.turn))) + \
                9   * (len(board.pieces(chess.QUEEN,board.turn)) - len(board.pieces(chess.QUEEN,not board.turn))) +  \
                5   * (len(board.pieces(chess.ROOK,board.turn)) - len(board.pieces(chess.ROOK,not board.turn))) + \
                3   * (len(board.pieces(chess.BISHOP,board.turn)) - len(board.pieces(chess.BISHOP,not board.turn))) + \
                3   * (len(board.pieces(chess.KNIGHT,board.turn)) - len(board.pieces(chess.KNIGHT,not board.turn))) + \
                1   * (len(board.pieces(chess.PAWN,board.turn)) - len(board.pieces(chess.PAWN,not board.turn))) + \
                0.1 * (len(list(board.legal_moves)) - temp_moves)
        #print(score)
        board.push(move)
        return score


    def alphaBetaMax(
        self, alpha, 
        beta, depth,
        cur_move, board:chess.Board
    ):
        ''' Max with the alpha beta algorithm
        '''
        #print('max: depth {}'.format(depth))
        if depth == 0:
            temp_score = self.eval_move_shannon(cur_move,board)
            #print('max score {}'.format(temp_score))
            return temp_score, cur_move
        best_move = cur_move
        for move in board.legal_moves:
            board.push(move)
            s, temp_move = self.alphaBetaMin(alpha, beta, depth-1,move,board)
            board.pop()
            if s >= beta:
                return beta, move # beta cuttoff
            if s > alpha:
                best_move = move
                alpha = s # max in minimax

        return alpha, best_move

    def alphaBetaMin(
        self, alpha, 
        beta, depth,
        cur_move, board:chess.Board
    ):
        ''' Min with the alpha beta algorithm
        '''
        #print('min depth {}'.format(depth))
        if depth == 0:
            temp_score = self.eval_move_shannon(cur_move,board)
            #print('min score {}'.format(temp_score))
            return temp_score, cur_move
        best_move = cur_move
        for move in board.legal_moves:
            board.push(move)
            s,temp_move = self.alphaBetaMax(alpha, beta, depth-1,move,board)
            board.pop()
            if s <= alpha:
                return alpha, move # alpha cutoff
            if s < beta:
                beta = s # min in minimax
                best_move = move
        return beta, best_move

   
    #def eval_pos(
    #    self, move, board
    #):
        """ Returns the score based off of a simple scoring algorithm 
              and a simple position matrix

        """
