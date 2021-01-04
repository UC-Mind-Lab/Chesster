"""The base class for a match within Chesster"""
import abc
import chess

from ..ai.base import BaseAI
from ..game.base import BaseGame
from ..records.match import MatchRecord
from ..timer.base import BaseTimer


class BaseMatch(abc.ABC):
    def __init__(self, white_ai:BaseAI, black_ai:BaseAI, 
            base_timer:BaseTimer, wins_required:int,
            initial_board_state:str=None) -> None:
        """The base match object for Chesster.

        Parameters
        ----------
        white_ai: BaseAI
            The AI for the white player.
        black_ai: BaseAI
            The AI for the black player.
        base_timer: BaseTimer
            The timer that will be copied for both players. Note
            that this object assumes that is a fresh timer object.
        initial_board_state: str=None
            The initial state of the board in FEN notation.
            If not specified it will default to the standard
            starting board state.
        """
        # Save the AI
        self.white_ai = white_ai
        self.black_ai = black_ai

        # Save the base timer
        self.base_timer = base_timer

        # Save the initial board state
        self._initial_board_state = initial_board_state

        # Create empty match record
        self._record = MatchRecord(wins_required)


    @property
    def record(self) -> MatchRecord:
        """The result of the match.
        If the match has yet to be played, it will be played first.

        Returns
        -------
        MatchRecord
            The record of the game.
        """
        if self._record.winner is None:
            self.play_game()
        return self._record


    @property
    def winner(self) -> chess.COLORS:
        """The result of the match.
        If the match has yet to be played, it will be played first.

        Returns
        -------
        chess.COLORS
            The color of the player that won the match.
        """
        if self._record.winner is None:
            self.play_game()
        return self._record.winner


    @abc.abstractmethod
    def _display(self) -> None:
        """This isn't technically required for the object to work
        correctly, but child classes have to at least explicitly set 
        this method to do nothing.
        """
        ...


    @abc.abstractmethod
    def _create_game(self) -> BaseGame:
        """Create a BaseGame object.
        In actually this will be overwritten to
        return the correct child class of BaseGame.

        Returns
        -------
        BaseGame
            The newly created base game.
        """
        ...


    def play_match(self) -> chess.COLORS:
        """Play the match!
        This includes displaying the match as it is played.

        Returns
        -------
        chess.COLORS
            The winner of the match.
        """
        # Have we already played?
        if self._record.winner is not None:
            # Yes, so simply return the result
            return self._record.winner

        # Play the match
        while self._record.winner is None:
            # Display match information
            self._display()
            # Create game
            game = self._create_game()
            # Start game
            game.play_game()
            # Save record of game
            self._record.append(game.record)
        # Display final result of match.
        self._display()
        return self._record.winner

