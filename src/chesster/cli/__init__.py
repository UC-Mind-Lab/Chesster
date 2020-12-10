#!/usr/bin/env python3
"""Command line interface with Chesster"""

import argparse
import cairosvg
import chess
import chess.svg
import os

from ..ai.random import RandomAI
from ..ai import AIs


class IllegalMove(Exception):
    def __init__(self, board: chess.Board, uci:str):
        self.board = board
        self.uci = uci

    def __str__(self):
        color = 'White' if self.board.color == chess.WHITE else 'Black'
        return f"{color} attempted illegal move {self.uci} "\
                f"in board:\n{self.board.fen()}"


class NonExistentAI(Exception):
    def __init__(self, ai:str): self.ai = ai

    def __str__(self):
        return f"{self.ai} is not a valid AI name. Valid AIs are "\
                f"{','.join(AIs.keys())}"


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


def main(white:str, black:str, save_dir:str="boards") -> int:
    """Main function.

    Parameters
    ----------
    white: str
        The name of the AI for the white player.
    black: str
        The name of the AI for the black player.
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

    # Setup white player
    try:
        whiteAI = AIs[white]()
    except KeyError:
        raise NonExistentAI(white)

    # Setup black player
    try:
        blackAI = AIs[black]()
    except KeyError:
        raise NonExistentAI(black)

    # Run game
    while not board.is_game_over():
        # Display the board
        color = "White" if board.turn == chess.WHITE else "Black"
        display_board(board, f"{color}'s move")
        save_board(board, save_dir)

        # Ask the AI to select a move
        if board.turn == chess.WHITE:
            move = whiteAI.make_move(board)
        else:
            move = blackAI.make_move(board)

        # Check that move is valid
        if not board.is_legal(move):
            raise IllegalMove(board, move, board)

        # Make the move
        board.push(move)

    # Display results
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
                    f"Available AIs:\n{','.join(sorted(AIs.keys()))}",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("white", help="The AI for the white player.")
    parser.add_argument("black", help="The AI for the white player.")
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
    except FileExistsError as exp:
        print(f"Directory \"{exp}\" already exists.", file=sys.stderr)
        exit(4)
    except PermissionError as exp:
        print(exp, file=sys.stderr)
        exit(5)


# Execute only if this file is being run as the entry file.
if __name__ == "__main__":
    cli_interface()

