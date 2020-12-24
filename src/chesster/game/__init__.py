"""Game module for Chesster"""

from .headless import HeadlessGame
from .visual import VisualGame

game_modes = {
    HeadlessGame.__name__: HeadlessGame,
    VisualGame.__name__: VisualGame
}


class NonExistentGame(Exception):
    def __init__(self, game:str):
        self.game = game

    def __str__(self):
        return f"{self.game} is not a valid Game name. Valid Games are "\
                f"{','.join(games.keys())}"

