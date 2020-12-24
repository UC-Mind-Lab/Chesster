"""A record of a game within Chesster"""
import chess
from .move import Move
from .result import GameResult


class GameEndedException(Exception):
    """Thrown if the game object was given the result, but more
    moves are attempted to be recorded.
    """
    def __str__(self):
        return "Moves can not be added if the game is over"


class GameRecord:
    def __init__(self, initial_board_state:chess.Board, 
            white_ai_type:str, black_ai_type: str):
        self.white_ai_type = white_ai_type
        self.black_ai_type = black_ai_type
        self.moves = [Move(None, None, None, initial_board_state)]
        self.result = None


    def append(self, new_move:Move) -> None:
        """Append a new move to the record

        Parameters
        ----------
        new_move: chesster.record.Move
            The move record to record.
        """
        if self.result is None:
            self.moves.append(new_move)
        else:
            raise GameEndedException

    
    def to_dict(self) -> dict:
        """Turn this class into a dictionary

        Returns
        -------
        dict
            This classes objects, but in dictionary form.
        """
        return {
            "initial_board_state": self.moves[0].board.fen(),
            "white_ai_type": self.white_ai_type,
            "black_ai_type": self.black_ai_type,
            "moves": [m.to_dict() for m in self.moves],
            "result": self.result.to_dict() \
                    if self.result else self.result
            }


    @classmethod
    def from_dict(cls, d:dict) -> 'GameResult':
        """Create a GameResult from a dictionary of values.

        Parameters
        ----------
        d: dict
            The dictionary of values

        Returns
        -------
        GameResult
            The created GameResult
        """
        gr = cls(
                initial_board_state =\
                        chess.Board(fen=d['initial_board_state']),
                white_ai_type = d['white_ai_type'],
                black_ai_type = d['black_ai_type']
                )

        moves = [Move.from_dict(m) for m in d['moves']]
        for m in moves[1:]:
            gr.append(m)
        
        if d['result']:
            gr.result = GameResult.from_dict(d['result'])

        return gr


