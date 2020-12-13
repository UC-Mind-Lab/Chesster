"""Increment timer object for Chesster."""
from .base import BaseTimer


class IncrementTimer(BaseTimer):
    def __init__(self, start_seconds:float, increment_seconds:float):
        """IncrementTimer

        Parameters
        ----------
        start_seconds: float
            The number of seconds the timer starts with.
        increment_seconds: float
            The number of seconds to increment after each move.
        """
        super().__init__(start_seconds, increment_seconds)


    @property
    def incrment_seconds(self) -> float:
        """Return the number of seconds that is added to the timer after each 
        move.

        Returns
        -------
        float
            The number of seconds that is added to the timer after each move.
        """
        return self._increment_seconds


    def stop(self) -> None:
        """Stop the timer

        Raises
        ------
        TimerError
            Raised if the timer is already running.
        """
        super().stop()
        # Check that the clock hasn't expired
        if self.alive:
            # Increment since the move is complete and timer is alive.
            self._seconds_left += self._increment_seconds

