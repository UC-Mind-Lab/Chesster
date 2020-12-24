"""Basic timer object for Chesster."""
from .base import BaseTimer
import numpy as np


class BasicTimer(BaseTimer):
    def __init__(self, *args):
        """BasicTimer
        Only keeps track of how much time has been used. It will thus never
        die.
        """
        super().__init__(np.inf, 0)


    def display_time(self) -> str:
        """Return nicely formatted string of minutes and seconds used.

        Returns
        -------
        str
            The number of minutes and seconds clocked on the timer
        """
        return self.seconds_to_string(self.time_clocked)


    def to_dict(self) -> dict:
        """Turn this class into a dictionary

        Returns
        -------
        dict
            This classes objects, but in dictionary form.
        """
        return {
                "class": self.__class__.__name__,
                "time_clocked": self._time_clocked
                }

