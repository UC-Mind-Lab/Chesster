"""The AI module for Chesster.
The base module implement the API for AIs, while
variants will use that API to compete in Chesster
"""
from .human import Human
from .random import RandomAI


AIs = {
    Human.__name__: Human,
    RandomAI.__name__: RandomAI
}

