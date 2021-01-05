"""A record of a move within Chesster"""
import chess
import copy

class Move:
    def __init__(self, move:chess.Move, color:chess.Color,
            time_used:float, board:chess.Board):
        """A record of a move within Chesster

        Parameters
        ----------
        move: chess.Move
            The move that was made.
        color: chess.Color
            The color of the player that made the move.
        time_used: float
            The number of seconds it took to calculate this move.
        board: chess.Board
            The state of the board after the move is applied.
        """
        self.move = move
        self.color = color
        self.time_used = time_used
        self.board = copy.deepcopy(board)


    @property
    def color_name(self) -> str:
        """The name of the color that made the move.

        Returns
        -------
        str
            The name of the color that made the move.
        """
        if self.color == chess.WHITE:
            return "White"
        else:
            return "Black"


    def to_dict(self) -> dict:
        """Turn this class into a dictionary

        Returns
        -------
        dict
            This classes objects, but in dictionary form.
        """
        return {
            "move": self.move.uci() if self.move else self.move,
            "color": self.color,
            "color_name": self.color_name,
            "time_used": self.time_used,
            "board": self.board.fen()
            }


    @classmethod
    def from_dict(cls, d:dict) -> 'Move':
        """Create a Move from a dictionary of values.

        Parameters
        ----------
        d: dict
            The dictionary of values

        Returns
        -------
        Move
            The move record that was created.
        """
        return cls(
                move = chess.Move.from_uci(d['move'])\
                        if d['move'] else d['move'],
                color = d['color'],
                time_used = d['time_used'],
                board = chess.Board(fen=d['board'])
                )

