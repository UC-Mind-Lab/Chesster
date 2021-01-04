"""The headless version of a game in Chesster"""

from ..ai.base import BaseAI
from ..timer.base import BaseTimer
from .base import BaseGame

class HeadlessGame(BaseGame):
    def __init__(self, white_ai:BaseAI, black_ai:BaseAI, 
            base_timer:BaseTimer, initial_board_state:str=None) -> None:
        # There is nothing to continually redraw for this
        # display mode.
        super().__init__(white_ai, black_ai, base_timer,
                continually_redraw_display=False,
                initial_board_state=initial_board_state)


    def _display(self) -> None:
        """Do nothing, just nothing"""
        pass

