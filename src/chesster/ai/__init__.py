"""The AI module for Chesster.
The base module implement the API for AIs, while
variants will use that API to compete in Chesster
"""
from .human import Human
from .random import RandomAI
from .ARCAI import ARCAI
from .bayley import BayleyAI
from .jeffbot import Jeffbot
from .joshai import SteinsGate
from .sid import Sid
from .tyler_westland import TylerWestlandAI
from .wayne import Wayne


AIs = {
    Human.__name__: Human,
    RandomAI.__name__: RandomAI,
    "Sid": Sid,
    ARCAI.__name__: ARCAI,
    BayleyAI.__name__: BayleyAI,
    Jeffbot.__name__: Jeffbot,
    SteinsGate.__name__: SteinsGate,
    TylerWestlandAI.__name__: TylerWestlandAI,
    Wayne.__name__: Wayne
}

class NonExistentAI(Exception):
    def __init__(self, ai:str):
        self.ai = ai

    def __str__(self):
        return f"{self.ai} is not a valid AI name. Valid AIs are "\
                f"{','.join(AIs.keys())}"

