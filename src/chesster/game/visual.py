"""The visual version of a game in Chesster"""
import chess
import chess.svg
import cairosvg
import PIL
import pygame
import os
import tempfile
import time

from ..ai.base import BaseAI
from ..timer.base import BaseTimer
from ..records.game import GameRecord
from ..records.result import GameResult
from .base import BaseGame


class VisualGame(BaseGame):
    def __init__(self, white_ai:BaseAI, black_ai:BaseAI, 
            base_timer:BaseTimer, initial_board_state:str=None,
            width:int=400, height:int=600, 
            screen:pygame.Surface=None, board_dir:str=None,
            frame_dir:str=None, output_gif:str=None, 
            win_screen_time:float=5,
            initial_pause_time:float=0
            ) -> None:
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
        initial_board_state: str=None
            The initial state of the board in FEN notation.
            If not specified it will default to the standard
        starting board state.
        width: int = 400
            The width of the window for PyGame.
        height: int = 600
            The height of the window for PyGame.
        screen: pygame.Surface
            The screen space to draw on, if not specified this object
            will create it's own. If given a screen it will assume that
            pygame has already been initialized. Note that this screen
            will override any values given for width and height.
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
        win_screen_time: float = 5
            The number of seconds to display win information.
        initial_pause_time: float=0
            Number of seconds to wait at the start of the match.
        """
        # Setup the super class portion
        super().__init__(white_ai, black_ai, base_timer,
                continually_redraw_display=True,
                initial_board_state=initial_board_state)

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
        if screen is None:
            # If no surface is defined we must initialize everything.
            pygame.init()
            self._screen = pygame.display.set_mode(
                    (width, height))
            # Display the empty screen for a bit
            start_time = time.perf_counter()
            while time.perf_counter() - start_time \
                    < initial_pause_time:
                self._display()
        else:
            self._screen = screen
        self._font = pygame.font.SysFont(None, 
                int(self._screen.get_height()/8))
        self._frame = 0
        self._win_screen_time = win_screen_time
        self._first_display = True
        self._initial_pause_time = initial_pause_time

        # Calculate inner widths and heights
        self._board_width = self._screen.get_width()
        self._board_height = (2.0/3.0) * self._screen.get_height()
        self._info_width = self._screen.get_width()
        self._info_height = (1.0/6.0) * self._screen.get_height()


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
        if self._record.result is None:
            # Play the game
            super().play_game()

            # Display the win screen for a bit
            start_time = time.perf_counter()
            while time.perf_counter() - start_time \
                    < self._win_screen_time:
                self._display()

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
        return self._record.result


    def _display_text(self, text:int, placement:tuple) -> None:
        """Render and display text.
        
        Parameters
        ----------
        text: str
            The text to render and display text
        placement: (int, int)
            The placement of the text on the screen.
        """
        # Render the text
        img = self._font.render(text, True, (255, 255, 255))
        # Display the text
        self._screen.blit(img, placement)


    def _display(self) -> None:
        """Draw to the PyGame screen, saving the board and frames if
        asked to.
        """
        # Eat the event, we do nothing with it though.
        pygame.event.get()
        # Black out the screen
        self._screen.fill((0,0,0))
        # Draw the board
        self._screen.blit(self._prep_board_sprite(), 
                (0,self._info_height))
        # Draw ai info
        self._draw_ai_info(chess.WHITE)
        self._draw_ai_info(chess.BLACK)
        # Push finished drawing of screen
        pygame.display.update()

        # Save frame
        if self._frame_dir is not None:
            pygame.image.save(pygame.display.get_surface(), 
                    os.path.join(self._frame_dir, f"{self._frame:08}.png"))
            self._frame += 1

        # Display the empty screen for a bit
        if self._first_display:
            self._first_display = False
            start_time = time.perf_counter()
            while time.perf_counter() - start_time \
                    < self._initial_pause_time:
                self._display()


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

        if len(self._board.move_stack) == 0:
            lastmove = None
        else:
            lastmove = self._board.move_stack[-1]

        cairosvg.svg2png(
                bytestring=chess.svg.board(
                    self._board,
                    lastmove=lastmove),
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
            start_height = self._screen.get_height()\
                    - self._info_height
            name = self.white_ai.__class__.__name__
            # Display the time
            info = self.white_timer.display_time()
            # Display win status if available.
            if self._record.result is not None:
                # Display win status
                if self._record.result.color == chess.WHITE:
                    info = f"{info} -- Win"
                else:
                    info = f"{info} -- Loss"
        else:
            start_height = 0
            name = self.black_ai.__class__.__name__
            # Display the time
            info = self.black_timer.display_time()
            # Display win status if available.
            if self._record.result is not None:
                # Display win status
                if self._record.result.color == chess.BLACK:
                    info = f"{info} -- Win"
                else:
                    info = f"{info} -- Loss"

        self._display_text(name, 
                (self._info_width*0.001, start_height))
        self._display_text(info,
                (self._info_width*0.001, start_height+\
                    (self._info_height/2.0)))

