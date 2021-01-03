"""Base Timer for Chesster"""
import abc
import time


class TimerError(Exception):
    """Thrown if start/stop are used in the incorrect way"""


class BaseTimer(abc.ABC):
    def __init__(self, start_seconds:float, increment_seconds:float):
        """BaseTimer

        Parameters
        ----------
        start_seconds: float
            The number of seconds the timer starts with.
        """
        self._start_seconds = start_seconds
        self._seconds_left = start_seconds
        self._start_time = None
        self._time_clocked = 0
        self._increment_seconds = increment_seconds
        self._elapsed_times = []


    def reset(self) -> None:
        """Resets all recorded values"""
        try:
            self.stop()
        except TimerError:
            # This error will occur if the timer wasn't
            # running.
            pass
        self._seconds_left = self._start_seconds
        self._time_clocked = 0
        self._elapsed_times = []


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
    def average_elapsed_time(self) -> float:
        """Return the average elapsed time

        Returns
        -------
        float
            The average elapsed time.
        """
        if len(self._elapsed_times) == 0:
            return None
        else:
            return sum(self._elapsed_times)/len(self._elapsed_times)


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
    def incrment_seconds(self) -> float:
        """Return the number of seconds that is added to the timer after each 
        move.

        Returns
        -------
        float
            The number of seconds that is added to the timer after each move.
        """
        return self._increment_seconds


    @property
    def time_clocked(self) -> float:
        """Return the number of seconds the timer has clocked

        Returns
        -------
        float
            The number of seconds the timer has clocked.
        """
        return self._time_clocked + self._elapsed_seconds()


    @staticmethod
    def seconds_to_string(seconds: float) -> str:
        """Return nicely formatted string of minutes, seconds, and milliseconds

        Parameters
        ----------
        seconds: float
            The number of seconds to convert

        Returns
        -------
        str
            The converted seconds
        """
        # Calculate the minutes and seconds
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        milliseconds = int(seconds % 60 % 1 * 100)
        # Return formatted text
        return f"{minutes:02}:{secs:02}:{milliseconds:02}"


    def display_time(self) -> str:
        """Return nicely formatted string of minutes and seconds left.

        Returns
        -------
        str
            The number of minutes and seconds left on the timer
        """
        return self.seconds_to_string(self.seconds_left)


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
        self._elapsed_times.append(elapsed)
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


    def to_dict(self) -> dict:
        """Turn this class into a dictionary
        Note it will not keep track of the currently started timer.

        Returns
        -------
        dict
            This classes objects, but in dictionary form.
        """
        return {
                "class": self.__class__.__name__,
                "start_seconds": self._start_seconds,
                "increment_seconds": self._increment_seconds,
                "seconds_left": self._seconds_left,
                "time_clocked": self._time_clocked,
                "elapsed_times": self._elapsed_times,
                "average_elapsed_time": self.average_elapsed_time
                }


    @classmethod
    def from_dict(cls, d:dict) -> 'BaseTimer':
        """Create a BaseTimer from a dictionary of values.

        Parameters
        ----------
        d: dict
            The dictionary of values

        Returns
        -------
        BaseTimer
            The created BaseTimer
        """
        t = cls(
                start_seconds = d['start_seconds'],
                increment_seconds = d['increment_seconds'],
            )
        t._seconds_left = d['seconds_left']
        t._time_clocked = d['time_clocked']
        t._elapsed_times = d['elapsed_times']
        return t

