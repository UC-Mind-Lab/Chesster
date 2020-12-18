"""Timer module for Chesster
The basic timer is the API for all other timers.
"""
from .basic import BasicTimer
from .bronstein import BronsteinDelayTimer
from .increment import IncrementTimer


timers = {
    BasicTimer.__name__: BasicTimer,
    BronsteinDelayTimer.__name__: BronsteinDelayTimer,
    IncrementTimer.__name__: IncrementTimer
}


class NonExistentTimer(Exception):
    def __init__(self, timer:str):
        self.timer = timer

    def __str__(self):
        return f"{self.timer} is not a valid timer name. Valid timers are "\
                f"{','.join(timers.keys())}"

