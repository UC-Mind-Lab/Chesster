"""The AI module for Chesster.
The base module implement the API for AIs, while
variants will use that API to compete in Chesster
"""
from .human import Human
from .random import RandomAI
from .tyler_westland import TylerWestlandAI


AIs = {
    Human.__name__: Human,
    RandomAI.__name__: RandomAI,
    TylerWestlandAI.__name__: TylerWestlandAI
}

class NonExistentAI(Exception):
    def __init__(self, ai:str):
        self.ai = ai

    def __str__(self):
        return f"{self.ai} is not a valid AI name. Valid AIs are "\
                f"{','.join(AIs.keys())}"

