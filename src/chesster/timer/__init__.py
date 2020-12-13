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
