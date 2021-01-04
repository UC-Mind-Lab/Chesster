"""The MatchRecord class for Chesster"""
import chess

from .game import GameRecord


class MatchEndedException(Exception):
    """Thrown if enough games have been completed for the match to be
    complete but another game is attempted to be recorded.
    """
    def __str__(self):
        return "Games can not be added if the match is over"


class MatchRecord:
    def __init__(self, wins_required:int):
        if wins_required < 1:
            raise ValueError("Wins required must be 1 or greater")
        self.wins_required = wins_required
        self.game_records = []


    def append(self, game_record:GameRecord) -> None:
        if game_record.result is None:
            raise ValueError("The result of an added GameRecord can be "\
                    "None. Please only add records of completed games")
        self.game_records.append(game_record)


    def _count_wins(self, color:chess.COLORS) -> int:
        """Count the number of wins for the given color.

        Parameters
        ----------
        color: chess.COLOR
            The color to count the wins for.

        Returns
        -------
        int
            The number of wins for the given color.
        """
        wins = 0
        for record in self.game_records:
            if record.result.color == color:
                wins += 1
        return wins


    @property
    def white_wins(self) -> int:
        return self._count_wins(chess.WHITE)


    @property
    def black_wins(self) -> int:
        return self._count_wins(chess.BLACK)


    @property
    def winner(self) -> chess.COLORS:
        """Return the match winner, None if no player has won.

        Returns
        -------
        chess.COLOR
            The color of the winner. Will be None if no player has won.
        """
        if self.white_wins >= self.wins_required:
            return chess.WHITE
        elif self.black_wins >= self.wins_required:
            return chess.BLACK
        else:
            return None

    @property
    def winner_name(self) -> str:
        """The name of the winning color.
        Will calculate it if not already calculated

        Returns
        -------
        str
            The name of the winning color.
        """
        if self.winner is None:
            return None
        elif self.winner == chess.WHITE:
            return "White"
        else:
            return "Black"


    @property
    def matches_played(self) -> int:
        return len(self.game_records)

    @property
    def expected_number_of_match(self) -> int:
        if self.wins_required == 1:
            return 1
        else:
            return self.wins_required*2 + 1


    def to_dict(self) -> dict:
        """Turn this class into a dictionary

        Returns
        -------
        dict
            This classes objects, but in dictionary form.
        """
        return {
            "wins_required": self.wins_required,
            "game_records": [gr.to_dict() for gr in self.game_records],
            "winner": self.winner,
            "white_wins": self.white_wins,
            "black_wins": self.black_wins
            }


    @classmethod
    def from_dict(cls, d:dict) -> 'MatchResult':
        """Create a MatchResult from a dictionary of values.

        Parameters
        ----------
        d: dict
            The dictionary of values

        Returns
        -------
        MatcResult
            The created MatchResult
        """
        mr = cls(
                wins_required=d['wins_required']
                )
        for game_record in d['game_records']:
            mr.append(GameRecord.from_dict(game_record))

        return mr

