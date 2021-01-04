"""The terminal version of a game in Chesster"""
import chess

from ..ai.base import BaseAI
from ..timer.base import BaseTimer
from .base import BaseGame

class TerminalGame(BaseGame):
    def __init__(self, white_ai:BaseAI, black_ai:BaseAI, 
            base_timer:BaseTimer, initial_board_state:str=None) -> None:
        # continually_redraw_display must be set to False
        # as this class uses basic print statements.
        super().__init__(white_ai, black_ai, base_timer,
                continually_redraw_display=False,
                initial_board_state=initial_board_state)


    def _display(self) -> None:
        """Do nothing, just nothing"""
        print("-"*20)
        print(self._board)
        if len(self._board.move_stack) > 0:
            print(f"Last Move: {self._board.move_stack[-1]}")
        if self._board.turn == chess.WHITE:
            timer_info = self.white_timer.display_time()
            color = "White"
        else:
            timer_info = self.black_timer.display_time()
            color = "Black"
        print(f"It is {color}'s turn")
        print(f"Timer: {timer_info}")

