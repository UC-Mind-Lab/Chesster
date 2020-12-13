"""Timer module for Chesster
The basic timer is the API for all other timers.
"""
from .basic import BasicTimer
from .increment import IncrementTimer


timers = {
    BasicTimer.__name__: BasicTimer,
    IncrementTimer.__name__: IncrementTimer
}
