"""The headless version of a game in Chesster"""

from .base import BaseGame

class HeadlessGame(BaseGame):
    def _display(self) -> None:
        """Do nothing, just nothing"""
        pass

