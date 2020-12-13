"""Bronstein delay timer object for Chesster."""
from .base import BaseTimer


class BronsteinDelayTimer(BaseTimer):
    def __init__(self, start_seconds:float, increment_seconds:float):
        """BronsteinDelayTimer

        Implements the Bronstein delay timer

        Parameters
        ----------
        start_seconds: float
            The number of seconds the timer starts with.
        increment_seconds: float
            The maximum number of seconds to increment after each move.
        """
        super().__init__(start_seconds)
        self._increment_seconds = increment_seconds


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
        elapsed = super().stop()
        # Check that the clock hasn't expired
        if self.alive:
            # Check that the elapsed seconds is more or equal to the increment
            if elapsed >= self._increment_seconds:
                # Add the maximum number of seconds
                self._seconds_left += self._increment_seconds
            else:
                # Add only the number of seconds used
                self._seconds_left += elapsed

