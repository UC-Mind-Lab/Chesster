"""Timer module for Chesster
The basic timer is the API for all other timers.
"""
from .increment import IncrementTimer

timers = {
    IncrementTimer.__name__: IncrementTimer
}
