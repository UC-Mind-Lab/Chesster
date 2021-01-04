"""The base class for a match within Chesster"""
import abc
import chess

from ..ai.base import BaseAI
from ..game.headless import HeadlessGame
from ..records.match import MatchRecord
from ..timer.base import BaseTimer
from .base import BaseMatch


class HeadlessMatch(BaseMatch):
    def _display(self) -> None:
        """This isn't technically required for the object to work
        correctly, but child classes have to at least explicitly set 
        this method to do nothing.
        """
        match_number = self._record.matches_played + 1
        print(
            f"Match: {match_number}/"\
            f"{self._record.expected_number_of_match};"\
            f"White wins: {self._record.white_wins};"\
            f"Black wins: {self._record.black_wins};",
            end="\r"
            )


    def _create_game(self) -> HeadlessGame:
        """Create a HeadlessGame object.

        Returns
        -------
        HeadlessGame
            The newly created headless game.
        """
        return HeadlessGame(self.white_ai, self.black_ai,
                self.base_timer, self._initial_board_state)

