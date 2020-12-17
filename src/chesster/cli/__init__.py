#!/usr/bin/env python3
"""Command line interface with Chesster"""

import argparse
import chess
import os

from ..ai.random import RandomAI
from ..ai import AIs
from ..timer import timers
from ..game.visual import VisualGame


class NonExistentAI(Exception):
    def __init__(self, ai:str):
        self.ai = ai

    def __str__(self):
        return f"{self.ai} is not a valid AI name. Valid AIs are "\
                f"{','.join(AIs.keys())}"


class NonExistentTimer(Exception):
    def __init__(self, timer:str):
        self.timer = timer

    def __str__(self):
        return f"{self.timer} is not a valid timer name. Valid timers are "\
                f"{','.join(timers.keys())}"


def main(white:str, black:str, timer:str="BronsteinDelayTimer", 
        start_seconds:int=600, increment_seconds:int=2, board_dir:str=None,
        frame_dir:str=None, output_gif:str=None, width:int=400,
        height:int=600) -> int:
    """Main function.

    Parameters
    ----------
    white: str
        The name of the AI for the white player.
    black: str
        The name of the AI for the black player.
    timer: str="BronsteinDelayTimer"
        The name of the timer for each player.
    start_seconds: float=600
        The number of seconds to start the timer at.
    increment_seconds: float=2
        The number of seconds to increment the timer after each move.
    board_dir: str=None
        The directory in which to save the images for the boards as the game 
        is played. If not specified it will be a temporary system folder.
    frame_dir: str=None
        The directory in which to save the images for the boards as the game 
        is played. If not specified it will be a temporary system folder.
    output_gif: str=None
        The name of the gif to output the whole game to.
    width: int=400
        The width of the PyGame window.
    height: int=600
        The height of the PyGame window.

    Returns
    -------
    int
        The exit code.

    Raises
    ------
    IllegalMove
        Occurs if an AI attempts a move that is illegal on the current
        board state
    NonExistentAI
        Occurs if white or black are not correct keys for known AIs.
    NonExistentTimer
        Occurs if the specified timer is not a correct key for known timers.
    FileExistsError
        Raised when the board_dir path already exists.
    PermissionError:
        Raised when there is insufficient permission to create/save files 
        with board_dir.
    """
    # Setup white player AI
    try:
        white_ai = AIs[white]()
    except KeyError:
        raise NonExistentAI(white)

    # Setup black player AI
    try:
        black_ai = AIs[black]()
    except KeyError:
        raise NonExistentAI(black)

    # Setup timers
    try:
        base_timer = timers[timer](start_seconds, increment_seconds)
    except KeyError:
        raise NonExistentTimer(timer)

    # Create the game object
    game = VisualGame(white_ai, black_ai, base_timer,
            width=width, height=height, board_dir=board_dir,
            frame_dir=frame_dir, output_gif=output_gif)

    # Play the game
    result = game.play_game()

    # Display results
    color = "White" if result.color == chess.WHITE else "Black"
    print(f"{color} won because of {result.reason}")
    
    # Return success code
    return 0


def parse_arguments(args=None) -> None:
    """Returns the parsed arguments.

    Parameters
    ----------
    args: List of strings to be parsed by argparse.
        The default None results in argparse using the values passed into
        sys.args.
    """
    parser = argparse.ArgumentParser(
            description="Chesster: Facilitate AIs to battle with chess. "\
                    f"Available AIs:\n{', '.join(sorted(AIs.keys()))}. "\
                    f"Available Timers:\n{', '.join(sorted(timers.keys()))}.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("white", help="The AI for the white player.")
    parser.add_argument("black", help="The AI for the white player.")
    parser.add_argument("--timer", default="BronsteinDelayTimer",
            help="The timer to use for players.")
    parser.add_argument("--start_seconds", default=600, type=float,
            help="The number of seconds to star the timer at.")
    parser.add_argument("--increment_seconds", default=2, type=float,
            help="The number of seconds to increment the timer after each move.")
    parser.add_argument("--board_dir", default=None,
            help="The directory to save the board images to. If not specified "\
            "it will be a temporary system folder.")
    parser.add_argument("--frame_dir", default=None,
            help="The directory to save the frame images to. If not specified "\
            "it will be a temporary system folder.")
    parser.add_argument("--output_gif", default=None,
            help="The name of the gif to save the whole game to.")
    parser.add_argument("--width", default=400, type=int,
            help="The width of the PyGame window.")
    parser.add_argument("--height", default=600, type=int,
            help="The height of the PyGame window.")
    args = parser.parse_args(args=args)
    return args


def cli_interface() -> None:
    """Get program arguments from command line and run main"""
    import sys
    args = parse_arguments()
    try:
        exit(main(**vars(args)))
    except NonExistentAI as exp:
        print(exp, file=sys.stderr)
        exit(1)
    except NonExistentTimer as exp:
        print(exp, file=sys.stderr)
        exit(2)
    except FileExistsError as exp:
        print(f"Directory \"{exp}\" already exists.", file=sys.stderr)
        exit(3)
    except PermissionError as exp:
        print(exp, file=sys.stderr)
        exit(4)


# Execute only if this file is being run as the entry file.
if __name__ == "__main__":
    cli_interface()

