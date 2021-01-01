"""The game result calculator for  Chesster"""
import chess

from ..game.exceptions import IllegalMove
from ..timer import timers
from ..timer.base import BaseTimer


class GameResult:
    def __init__(self, board: chess.Board, white_timer:BaseTimer,
            black_timer:BaseTimer, illegal_move:'IllegalMove'=None):
        """An object that determines and explains the winner of a game.

        Parameters
        ----------
        board: chess.Board
           The board in it's end state
        white_timer: BaseTimer
            The timer associated with the white player.
        black_timer: BaseTimer
            The timer associated with the black player.
        illegal_move: IllegalMove = None
            The IllegalMove exception that caused the game to end, if
            applicable.
        """
        self.board = board
        self.white_timer = white_timer
        self.black_timer = black_timer
        self.illegal_move = illegal_move

        self._color = None
        self._reason = None
        self._short_reason = None


    def _determine_winner(self) -> None:
        """Analyze the board and timers to determine winner.
        Save the result in self._color and self._reason
        """
        # Was it a simple checkmate?
        if self.board.is_checkmate():
            self._color = not self.board.turn
            self._short_reason = self._reason = "checkmate"
        else:
            if self.illegal_move is not None:
                self._color = not self.illegal_move.offending_color
                self._short_reason = self._reason = "illegal move"
            else:
                # Check for time outs
                if not self.black_timer.alive:
                    self._color = chess.WHITE
                    self._short_reason = self._reason = "time out"
                elif not self.white_timer.alive:
                    self._color = chess.BLACK
                    self._short_reason = self._reason = "time out"
                # Compare time left on timer
                elif self.white_timer.seconds_left \
                        > self.black_timer.seconds_left:
                    self._color = chess.WHITE
                    self._reason = "more time on timer"
                    self._short_reason = "timer"
                elif self.black_timer.seconds_left \
                        > self.white_timer.seconds_left:
                    self._color = chess.BLACK
                    self._reason = "more time on timer"
                    self._short_reason = "timer"

                # Compare total time spent
                elif self.white_timer.time_clocked \
                        < self.black_timer.time_clocked:
                    self._color = chess.WHITE
                    self._reason = "less time computing"
                    self._short_reason = "compute time"
                elif self.black_timer.time_clocked \
                        < self.white_timer.time_clocked:
                    self._color = chess.BLACK
                    self._reason = "less time computing"
                    self._short_reason = "compute time"
                else:
                    # Complete tie, nothing can be done
                    self._color = None
                    self._reason = "total tie"
                    self._short_reason = "total tie"


    @property
    def color(self) -> chess.COLORS:
        """The winning color.
        Will calculate it if not already calculated

        Returns
        -------
        chess.COLORS
            The winning color.
        """
        if self._color is None:
            self._determine_winner()
        return self._color


    @property
    def reason(self) -> str:
        """The logic behind the winner
        Will calculate it if not already calculated

        Returns
        -------
        str 
            The explanation for why the color won.
        """
        if self._reason is None:
            self._determine_winner()
        return self._reason


    @property
    def short_reason(self) -> str:
        """The logic behind the winner
        Will calculate it if not already calculated

        Returns
        -------
        str 
            The short explanation for why the color won.
        """
        if self._short_reason is None:
            self._determine_winner()
        return self._short_reason


    def to_dict(self) -> dict:
        """Turn this class into a dictionary

        Returns
        -------
        dict
            This classes objects, but in dictionary form.
        """
        return {
            "board": self.board.fen(),
            "white_timer": self.white_timer.to_dict(),
            "black_timer": self.black_timer.to_dict(),
            "illegal_move": self.illegal_move.to_dict() \
                    if self.illegal_move else self.illegal_move,
            "color": self.color,
            "reason": self.reason,
            "short_reason": self.short_reason
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
        return cls(
                board = chess.Board(fen=d['board']),
                white_timer = timers[d['white_timer']['class']].\
                        from_dict(d['white_timer']),
                black_timer = timers[d['black_timer']['class']].\
                        from_dict(d['black_timer']),
                illegal_move = IllegalMove.from_dict(d['illegal_move'])\
                        if d['illegal_move'] else d['illegal_move']
                )

