"""The visual version of a game in Chesster"""
import chess
import chess.svg
import cairosvg
import PIL
import pygame
import os
import tempfile

from ..ai.base import BaseAI
from ..timer.base import BaseTimer
from .base import BaseGame, GameResult


class VisualGame(BaseGame):
    def __init__(self, white_ai:BaseAI, black_ai:BaseAI, 
            base_timer:BaseTimer, width:int=400, height:int=600, 
            board_dir:str=None, frame_dir:str=None,
            output_gif:str=None) -> None:
        """Play the game with a visual output, using PyGame.

        Parameters
        ----------
        white_ai: BaseAI
            The AI for the white player.
        black_ai: BaseAI
            The AI for the black player.
        base_timer: BaseTimer
            The timer that will be copied for both players. Note
            that this object assumes that is a fresh timer object.
        width: int = 400
            The width of the window for PyGame.
        height: int = 600
            The height of the window for PyGame.
        board_dir: str = None
            If specified it's the directory to save the PNG of each
            board state. Else they're stored in a temporary directory
            that is deleted after this object is destroyed.
        frame_dir: str = None
            If specified it's the directory to save the PNG of each
            frame that PyGame displays. Else they're either not stored
            at all or stored in a temporary directory that is deleted 
            after this object is destroyed. Their storage is used in
            creating the output_gif.
        output_gif: str = None
            If specified the PNG of each frame that PyGame displays is
            turned into a GIF and stored at the specified location.
        """
        # Setup the super class portion
        super().__init__(white_ai, black_ai, base_timer)

        # Save the output directory/file names
        self._board_dir = board_dir
        self._frame_dir = frame_dir
        self._output_gif = output_gif
        # Setup the output directories
        # Temporary or specified folder for board images?
        if self._board_dir is not None:
            if os.path.exists(self._board_dir):
                raise FileExistsError(self._board_dir)
            else:
                os.mkdir(self._board_dir)
        else:
            self._board_dir_handle = tempfile.\
                    TemporaryDirectory(prefix="chesster_board_")
            self._board_dir = self._board_dir_handle.name

        # If the user wants to keep the frames, does the folder already 
        # exist?
        if self._frame_dir is not None:
            if os.path.exists(self._frame_dir):
                raise FileExistsError(self._frame_dir)
            else:
                os.mkdir(self._frame_dir)
        elif output_gif is not None:
            self._frame_dir_handle = tempfile.\
                    TemporaryDirectory(prefix="chesster_frame_")
            self._frame_dir = self._frame_dir_handle.name

        # Check if the output gif (if specified) already exists
        if self._output_gif is not None:
            if os.path.exists(self._output_gif):
                raise FileExistsError(self._output_gif)

        # Initialize PyGame
        self._width = width
        self._height = height
        pygame.init()
        self._screen = pygame.display.set_mode((self._width, self._height))
        self._font = pygame.font.SysFont(None, int(self._height*(1/8)))
        self._frame = 0

        # Calculate inner widths and heights
        self._board_width = self._width
        self._board_height = (2.0/3.0) * self._height
        self._info_width = self._width
        self._info_height = (1.0/6.0) * self._height


    def play_game(self) -> GameResult:
        """Play the game!
        This has been extended so that the output_gif is created
        at the end if has been specified.

        Returns
        -------
        GameResult
            The result of the game. It's also saved to self._result
        """
        # Has the game been played yet?
        if self._result is None:
            # Play the game
            super().play_game()

            # Save all the frames into a gif (if applicable)
            if self._output_gif is not None:
                # Opening up every frame and keeping them open will
                # result in too many files being open.
                def frames_iter():
                    for root, dirs, files in os.walk(self._frame_dir,
                            topdown=False):
                        for image in sorted(files):
                            yield PIL.Image.open(os.path.join(root, image))
                it = frames_iter()
                first = next(it)
                first.save(self._output_gif,
                           save_all=True,
                           append_images=it,
                           duration=10,
                           loop=0)
        # Return the result
        return self._result


    def _display(self) -> None:
        """Draw to the PyGame screen, saving the board and frames if
        asked to.
        """
        # Black out the screen
        self._screen.fill((0,0,0))
        # Draw the board
        self._screen.blit(self._prep_board_sprite(), (0,self._info_height))
        # Draw ai info
        self._draw_ai_info(chess.WHITE)
        self._draw_ai_info(chess.BLACK)
        # Push finished drawing of screen
        pygame.display.update()
        # Save frame
        if self._frame_dir is not None:
            pygame.image.save(self._screen, os.path.join(
                self._frame_dir, 
                f"{self._frame:08}.png"))
            self._frame += 1


    def _prep_board_sprite(self) -> pygame.Surface:
        """Display the given board.
        Note this function makes use of it's scope within main.

        Returns
        -------
        pygame.Surface
           The object that the board is rendered to. 
        """
        # 2/3 of the screen is the board, the other 1/3 are for info
        # above (1/6) and below (1/6) of the board.
        board_img_path = self._save_board()
        return pygame.image.load(board_img_path)


    def _save_board(self) -> str:
        """Save the given board in the given directory.
        File name will be the current turn number.

        Returns
        -------
        str
            The path to the saved image of the board
        """
        save_name=os.path.join(self._board_dir, 
                f"{len(self._board.move_stack):06}.png")
        cairosvg.svg2png(
                bytestring=chess.svg.board(self._board),
                write_to=save_name,
                parent_width=self._board_width, 
                parent_height=self._board_height)
        return save_name


    def _draw_ai_info(self, color:chess.COLORS) -> None:
        """Draw the info for the AI of the specified AI color
        Parameters
        ----------
        color: chess.COLORS
            The color to draw the info of.
        """
        # Collect relevant info
        if color == chess.WHITE:
            name = self.white_ai.__class__.__name__
            time = self.white_timer.display_time()
            start_height = self._height - self._info_height
        else:
            name = self.black_ai.__class__.__name__
            time = self.black_timer.display_time()
            start_height = 0

        # Render images
        name_img = self._font.render(name, True, (255,255,255))
        time_img = self._font.render(time, True, (255,255,255))

        # Calculate image placements
        name_placment = (self._info_width*0.001, start_height)
        time_placment = (self._info_width*0.001,
                start_height+(self._info_height/2.0))
        # Display images
        self._screen.blit(name_img, name_placment)
        self._screen.blit(time_img, time_placment)

