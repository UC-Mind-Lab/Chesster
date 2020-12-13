"""Basic timer object for Chesster."""
from .base import BaseTimer
import numpy as np


class BasicTimer(BaseTimer):
    def __init__(self):
        """BasicTimer
        Only keeps track of how much time has been used. It will thus never
        die.
        """
        super().__init__(np.inf)

