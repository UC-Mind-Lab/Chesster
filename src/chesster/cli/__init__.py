#!/usr/bin/env python3
"""Command line interface with Chesster"""

import argparse
import cairosvg
import chess
import chess.svg
import multiprocessing as mp
import os
import PIL
import pygame
import tempfile

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


def save_board(board:chess.Board, board_dir:str, width:int, height:int) -> str:
    """Save the given board in the given directory.
    File name will be the current turn number.

    Parameters
    ----------
    board: chess.Board
        The board to display.
    board_dir: str
        The directory to save the file within.
    width: int
        The width of the image to save.
    height: int
        The height of the image to save.

    Returns
    -------
    str
        The path to the saved image of the board
    """
    save_name=os.path.join(board_dir, f"{len(board.move_stack):06}.png")
    cairosvg.svg2png(bytestring=chess.svg.board(board), write_to=save_name,
            parent_width=width, parent_height=height)
    return save_name


def main(white:str, black:str, timer:str="IncrementTimer", 
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
    timer: str="IncrementTimer"
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
    # Temporary or specified folder for board images?
    if board_dir is not None:
        if os.path.exists(board_dir):
            raise FileExistsError(board_dir)
        else:
            os.mkdir(board_dir)
    else:
        board_dir_handle = tempfile.TemporaryDirectory(prefix="chesster_board_")
        board_dir = board_dir_handle.name

    # If the user wants to keep the frames, does the folder already exist?
    if frame_dir is not None:
        if os.path.exists(frame_dir):
            raise FileExistsError(frame_dir)
        else:
            os.mkdir(frame_dir)
    elif output_gif is not None:
        frame_dir_handle = tempfile.TemporaryDirectory(prefix="chesster_frame_")
        frame_dir = frame_dir_handle.name

    # Check if the output gif (if specified) already exists
    if output_gif is not None:
        if os.path.exists(output_gif):
            raise FileExistsError(output_gif)

    # Generate a default board
    board = chess.Board()

    # Create Queues for communication with AI in separate thread
    queue = mp.Queue()
    # Create empty process variable to determine if one is running or not
    aiProcess = None

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

    # Initialize PyGame
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    font = pygame.font.SysFont(None, int(height*(1/8)))
    frame = 0

    # Prep sprite of board
    def prep_board_sprite():
        """Display the given board.
        Note this function makes use of it's scope within main.
        """
        # 2/3 of the screen is the board, the other 1/3 are for info
        # above (1/6) and below (1/6) of the board.
        board_img_path = save_board(board, board_dir, width, height*(2/3))
        return pygame.image.load(board_img_path)


    def draw(frame=[0]) -> None:
        """Draw everything on the screen.
        Note this function makes use of it's scope within main.
        
        The board is structured as 1/6 of height of the bottom and top are for
        info about the players.
        The remaining 2/3 of height is for the board.

        Parameters
        ----------
        frame
            This is a bad hack to implement a consistent variable when
            ever this method is called. It will be removed when this
            entire file is refactored. It is here currently as the author
            is unfamiliar with PyGame, and this is all basically a proof
            of concept.
        """
        def draw_ai_info(color:chess.COLORS) -> None:
            """Draw the info for the AI of the specified AI color
            Parameters
            ----------
            color: chess.COLORS
                The color to draw the info of.
            """
            # Collect relevant info
            if color == chess.WHITE:
                name = whiteAI.__class__.__name__
                time = whiteTimer.display_time()
                start_height = height*5/6
            else:
                name = blackAI.__class__.__name__
                time = blackTimer.display_time()
                start_height = 0

            # Render images
            name_img = font.render(name, True, (255,255,255))
            time_img = font.render(time, True, (255,255,255))
            # Calculate image placements
            name_placment = (width*0.001, start_height)
            time_placment = (width*0.001, start_height+(height*(1/12)))
            # Display images
            screen.blit(name_img, name_placment)
            screen.blit(time_img, time_placment)

            
        # Black out the screen
        screen.fill((0,0,0))
        # Draw the board
        screen.blit(prep_board_sprite(), (0,height*(1/6)))
        # Draw ai info
        draw_ai_info(chess.WHITE)
        draw_ai_info(chess.BLACK)
        # Push finished drawing of screen
        pygame.display.update()
        # Save frame
        if frame_dir is not None:
            pygame.image.save(screen, os.path.join(
                frame_dir, 
                f"{frame[0]:08}.png"))
            frame[0] += 1

    # Run until told to quit
    while True:
        # Check for events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Clean exit
                return 0

        # Draw the board.
        draw()

        # Is game still valid?
        if board.is_game_over() or not whiteTimer.alive or not blackTimer.alive:
            # Game over
            break
        else:
            # Has the AI computed their move?
            if queue.qsize() >= 1:
                # Stop the timer
                if board.turn == chess.WHITE:
                    whiteTimer.stop()
                else:
                    blackTimer.stop()

                # Remove the move from the queue
                move = queue.get()

                # Delete the previous AI process
                aiProcess = None

                # Check that move is valid
                if not board.is_legal(move):
                    raise IllegalMove(board, move)

                # Make the move
                board.push(move)

            # Does an AI process already exist?
            elif aiProcess is not None:
                # Do nothing, we're simply waiting
                pass
            # There is no move available, nor is there a process running.
            else:
                def request_move(q:mp.Queue, board:chess.Board, ai:'BaseAi', 
                        timer:'BaseTimer') -> None:
                    """Actions for an AI thread to perform.
                    Parameters
                    ----------
                    q: multiprocessing.Queue
                        The queue to push the calculated move to.
                    board: chess.Board
                        The board the AI will be calculating a move upon.
                    ai: chesster.ai.base.BaseAI
                        A Chesster AI that will calculate a move.
                    timer: chesster.timer.base.BaseTimer
                        The timer associated with the AI
                    """
                    move = ai.make_move(board, timer)
                    q.put(move)

                # Ask the AI to select a move
                if board.turn == chess.WHITE:
                    whiteTimer.start()
                    aiProcess = mp.Process(
                            target=request_move,
                            args=(queue, board, whiteAI, whiteTimer))
                else:
                    blackTimer.start()
                    aiProcess = mp.Process(
                            target=request_move,
                            args=(queue, board, blackAI, blackTimer))
                # Start the process
                aiProcess.start()


    # Display results
    if not whiteTimer.alive:
        print("White ran out of time!")
    elif not blackTimer.alive:
        print("Black ran out of time!")
    else:
        print(f"Game Over\nResult: {board.result()}")

    # Save all the frames into a gif (if applicable)
    if output_gif is not None:
        def frames_iter():
            for root, dirs, files in os.walk(frame_dir, topdown=False):
                for image in sorted(files):
                    yield PIL.Image.open(os.path.join(root, image))
        it = frames_iter()
        first = next(it)
        first.save(output_gif,
                   save_all=True,
                   append_images=it,
                   duration=10,
                   loop=0)
    
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
    parser.add_argument("--timer", default="IncrementTimer",
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

