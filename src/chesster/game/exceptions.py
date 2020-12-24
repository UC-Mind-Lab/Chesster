"""The exceptions within the game class"""
import chess


class IllegalMove(Exception):
    def __init__(self, board: chess.Board, move: chess.Move):
        """An exception for illegal moves.

        Parameters
        ----------
        board: chess.Board
            The board the move was attempted on.
        move: chess.Move
            The move that was attempted.
        """
        self.board = board
        self.move = move


    @property
    def offending_color(self) -> chess.Color:
        """The color that made the illegal move"""
        return self.board.color


    @property
    def offending_color_name(self) -> str:
        """The name of the color that made the illegal move"""
        return 'White' if self.offending_color == chess.WHITE else 'Black'


    def __str__(self) -> str:
        return f"{self.offending_color_name} attempted illegal move "\
            f"{self.move.uci()} in board:\n{self.board.fen()}"


    def to_dict(self) -> dict:
        """Turn this class into a dictionary

        Returns
        -------
        dict
            This classes objects, but in dictionary form.
        """
        return {
                "board": self.board.fen(),
                "move": self.move.uci()
                }


    @classmethod
    def from_dict(cls, d:dict) -> 'IllegalMove':
        """Create an IllegalMove from a dictionary of values.

        Parameters
        ----------
        d: dict
            The dictionary of values

        Returns
        -------
        IllegalMove
            The created IllegalMove
        """
        return cls(
                board = chess.Board(fen=d['board']),
                move = chess.Move.from_uci(d['move'])
                )

