"""The AI module for Chesster.
The base module implement the API for AIs, while
variants will use that API to compete in Chesster
"""
from .random import RandomAI


AIs = {
    RandomAI.__name__: RandomAI
}

