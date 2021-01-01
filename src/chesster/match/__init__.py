"""Match module for Chesster"""

from .headless import HeadlessMatch
from .visual import VisualMatch

match_modes = {
    "headless": HeadlessMatch,
    "visual": VisualMatch
}


class NonExistentMatch(Exception):
    def __init__(self, match:str):
        self.match = match

    def __str__(self):
        return f"{self.match} is not a valid Match mode name. Valid "\
                f"Match modes are {','.join(match_modes.keys())}"

