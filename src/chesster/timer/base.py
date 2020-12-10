"""Base Timer for Chesster"""
import abc
import time


class TimerError(Exception):
    """Thrown if start/stop are used in the incorrect way"""


class BaseTimer(abc.ABC):
    def __init__(self, start_seconds:float):
        """BaseTimer

        Parameters
        ----------
        start_seconds: float
            The number of seconds the timer starts with.
        """
        self._seconds_left = start_seconds
        self._start_time = None


    @property
    def alive(self) -> bool:
        """Return rather there is still time on the timer.

        Returns
        -------
        bool
            Rather there is still time on the timer.
        """
        return self.seconds_left > 0


    @property
    def seconds_left(self) -> float:
        """Return the number of seconds left

        Returns
        -------
        float
            The number of seconds left on the timer
        """
        return self._seconds_left - self._elapsed_seconds()


    def start(self) -> None:
        """Start the timer

        Raises
        ------
        TimerError
            Raised if the timer is already running.
        """
        if self._start_time is not None:
            raise TimerError("Timer is already running")
        self._start_time = time.perf_counter()


    def stop(self) -> None:
        """Stop the timer

        Raises
        ------
        TimerError
            Raised if the timer is already running.
        """
        if self._start_time is None:
            raise TimerError("Timer is not running")
        self._seconds_left -= self._elapsed_seconds()
        self._start_time = None


    def _elapsed_seconds(self) -> float:
        """Seconds elapsed since timer started.

        Returns
        -------
        float
            The number of seconds elapsed since the timer started.
        """
        if self._start_time is None:
            return 0
        else:
            return time.perf_counter() - self._start_time

