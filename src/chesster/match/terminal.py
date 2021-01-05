"""The terminal version for a match within Chesster"""
import abc
import chess

from ..ai.base import BaseAI
from ..game.terminal import TerminalGame
from ..records.match import MatchRecord
from ..timer.base import BaseTimer
from .base import BaseMatch


class TerminalMatch(BaseMatch):
    def _display(self) -> None:
        """This isn't technically required for the object to work
        correctly, but child classes have to at least explicitly set 
        this method to do nothing.
        """
        info = ""
        match_number = self._record.matches_played + 1
        if self._record.winner is None:
            if match_number <= self._record.expected_number_of_match:
                info += f"Match: {match_number}/"\
                    f"{self._record.expected_number_of_match}\n"
            info += "White wins: {self._record.white_wins}\n"
            info += "Black wins: {self._record.black_wins}\n"

            if match_number > 1:
                result = self._record.game_records[-1].result
                info += f"{result.color_name} won because: "\
                        f"{result.reason}\n"

        else:
            info += f"Winner of whole match is {self._record.winner_name}"

        print(info)


    def _create_game(self) -> TerminalGame:
        """Create a HeadlessGame object.

        Returns
        -------
        HeadlessGame
            The newly created headless game.
        """
        return TerminalGame(self.white_ai, self.black_ai,
                self.base_timer, self._initial_board_state)

