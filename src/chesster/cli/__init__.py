#!/usr/bin/env python3
"""Command line interface with Chesster"""

import argparse
import chess
import os


def main() -> int:
    """Main function.

    Parameters
    ----------
    Returns
    -------
    int
        The exit code.
    """

    # Generate a default board
    board = chess.Board()

    # Print it out
    print(board)
    
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
            description="Chesster: Facilitate AIs to battle with chess.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args = parser.parse_args(args=args)
    return args


def cli_interface() -> None:
    """Get program arguments from command line and run main"""
    import sys
    args = parse_arguments()
    try:
        exit(main(**vars(args)))
    except FileNotFoundError as exp:
        print(exp, file=sys.stderr)
        exit(-1)


# Execute only if this file is being run as the entry file.
if __name__ == "__main__":
    cli_interface()

