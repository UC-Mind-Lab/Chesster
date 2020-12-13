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
        self._time_clocked = 0


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


    @property
    def time_clocked(self) -> float:
        """Return the number of seconds the timer has clocked

        Returns
        -------
        float
            The number of seconds the timer has clocked.
        """
        return self._time_clocked + self._elapsed_seconds()


    def display_time(self) -> str:
        """Return nicely formatted string of minutes and seconds left.

        Returns
        -------
        str
            The number of minutes and seconds left on the timer
        """
        # Get the time left at this exact moment of the method call
        seconds_left = self.seconds_left
        # Calculate the minutes and seconds
        minutes = int(seconds_left // 60)
        seconds = int(seconds_left % 60)
        milliseconds = int(seconds_left % 60 % 1 * 100)
        # Return formatted text
        return f"{minutes:02}:{seconds:02}:{milliseconds:02}"


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


    def stop(self) -> float:
        """Stop the timer

        Returns
        -------
        float
            The number of seconds that passed from start to stop.

        Raises
        ------
        TimerError
            Raised if the timer is already running.
        """
        if self._start_time is None:
            raise TimerError("Timer is not running")
        elapsed = self._elapsed_seconds()
        self._seconds_left -= elapsed
        self._time_clocked += elapsed
        self._start_time = None
        # Return the number of seconds that elapsed
        return elapsed


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

