#!/usr/bin/env python3
"""Command line interface with Chesster"""

import argparse
import cairosvg
import chess
import chess.svg
import os

from ..ai.random import RandomAI
from ..ai import AIs
from ..timer import timers


class IllegalMove(Exception):
    def __init__(self, board: chess.Board, uci:str):
        self.board = board
        self.uci = uci

    def __str__(self):
        color = 'White' if self.board.color == chess.WHITE else 'Black'
        return f"{color} attempted illegal move {self.uci} "\
                f"in board:\n{self.board.fen()}"


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


def display_board(board:chess.Board, message:str) -> None:
    """Display the given board.

    Parameters
    ----------
    board: chess.Board
        The board to display.
    message: str
        The extra message to display.
    """
    print(board)
    print(message)
    print("-"*16)


def save_board(board:chess.Board, save_dir:str) -> str:
    """Save the given board in the given directory.
    File name will be the current turn number.

    Parameters
    ----------
    board: chess.Board
        The board to display.
    save_dir: str
        The directory to save the file within.
    """
    save_name=os.path.join(save_dir, f"{len(board.move_stack):06}.png")
    cairosvg.svg2png(bytestring=chess.svg.board(board), write_to=save_name)


def main(white:str, black:str, timer:str="IncrementTimer", start_seconds:int=600,
        increment_seconds:int=2, save_dir:str="boards") -> int:
    """Main function.

    Parameters
    ----------
    white: str
        The name of the AI for the white player.
    black: str
        The name of the AI for the black player.
    timer: str
        The name of the timer for each player.
    start_seconds: float=600
        The number of seconds to start the timer at.
    increment_seconds: float=2
        The number of seconds to increment the timer after each move.
    save_dir: str = "boards"
        The directory in which to save the images for the boards as the game 
        is played.

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
        Raised when the save_dir path already exists.
    PermissionError:
        Raised when there is insufficient permission to create/save files 
        with save_dir.
    """
    # Ensure that the save_dir doesn't already exist
    if os.path.exists(save_dir):
        raise FileExistsError(save_dir)
    else:
        os.mkdir(save_dir)

    # Generate a default board
    board = chess.Board()

    # Setup white player AI
    try:
        whiteAI = AIs[white]()
    except KeyError:
        raise NonExistentAI(white)

    # Setup black player AI
    try:
        blackAI = AIs[black]()
    except KeyError:
        raise NonExistentAI(black)

    # Setup timers
    try:
        whiteTimer = timers[timer](start_seconds, increment_seconds)
        blackTimer = timers[timer](start_seconds, increment_seconds)
    except KeyError:
        raise NonExistentTimer(timer)

    # Run game
    while not board.is_game_over() and whiteTimer.alive and blackTimer.alive:
        # Display the board
        if board.turn == chess.WHITE:
            color = "White"
            time_left = whiteTimer.seconds_left
        else:
            color = "Black"
            time_left = blackTimer.seconds_left
        display_board(board, f"{color}'s move with {time_left} seconds left.")
        save_board(board, save_dir)

        # Ask the AI to select a move
        if board.turn == chess.WHITE:
            whiteTimer.start()
            move = whiteAI.make_move(board, whiteTimer)
            whiteTimer.stop()
        else:
            blackTimer.start()
            move = blackAI.make_move(board, blackTimer)
            blackTimer.stop()

        # Check that move is valid
        if not board.is_legal(move):
            raise IllegalMove(board, move, board)

        # Make the move
        board.push(move)

    # Display results
    if not whiteTimer.alive:
        print("White ran out of time!")
    elif not blackTimer.alive:
        print("Black ran out of time!")
    else:
        display_board(board, f"Game Over\nResult: {board.result()}")
        save_board(board, save_dir)
    
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
            description="Chesster: Facilitate AIs to battle with chess."\
                    f"Available AIs:\n{','.join(sorted(AIs.keys()))}"\
                    f"Available Timers:\n{','.join(sorted(timers.keys()))}",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("white", help="The AI for the white player.")
    parser.add_argument("black", help="The AI for the white player.")
    parser.add_argument("--timer", default="IncrementTimer",
            help="The timer to use for players.")
    parser.add_argument("--start_seconds", default=600, type=float,
            help="The number of seconds to star the timer at.")
    parser.add_argument("--increment_seconds", default=2, type=float,
            help="The number of seconds to increment the timer after each move.")
    parser.add_argument("--save_dir", default="boards",
            help="The directory to save the board images to.")
    args = parser.parse_args(args=args)
    return args


def cli_interface() -> None:
    """Get program arguments from command line and run main"""
    import sys
    args = parse_arguments()
    try:
        exit(main(**vars(args)))
    except IllegalMove as exp:
        print(exp, file=sys.stderr)
        if exp.board.turn == chess.WHITE:
            exit(1)
        else:
            exit(2)
    except NonExistentAI as exp:
        print(exp, file=sys.stderr)
        exit(3)
    except NonExistentTimer as exp:
        print(exp, file=sys.stderr)
        exit(4)
    except FileExistsError as exp:
        print(f"Directory \"{exp}\" already exists.", file=sys.stderr)
        exit(5)
    except PermissionError as exp:
        print(exp, file=sys.stderr)
        exit(6)


# Execute only if this file is being run as the entry file.
if __name__ == "__main__":
    cli_interface()

