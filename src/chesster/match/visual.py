"""The Visual class for a match within Chesster"""
import abc
import chess
import os
import PIL
import pygame
import tempfile
import time

from ..ai.base import BaseAI
from ..timer.base import BaseTimer
from ..game.visual import VisualGame
from .base import BaseMatch


class VisualMatch(BaseMatch):
    def __init__(self, white_ai:BaseAI, black_ai:BaseAI, 
            base_timer:BaseTimer, wins_required:int,
            initial_board_state:str=None,
            width:int=800, height:int=600, 
            board_subsurface:pygame.Surface=None, 
            match_info_subsurface:pygame.Surface=None, 
            boards_dir:str=None, frames_dir:str=None,
            output_gif:str=None, win_screen_time:float=5,
            initial_pause_time:float=0
            ) -> None:
        """Play a match of games with a visual output, using PyGame.

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
        width: int = 800
            The width of the window for PyGame.
        height: int = 600
            The height of the window for PyGame.
        board_subsurface: pygame.Surface
            The screen space to draw the board on.
            It will be assumed that PyGame was initialized 
                if this is given.
            This object is passed onto the VisualGame
                object for use.
            This object does nothing with it.
            If not passed then one will be created.
            It will be half the width of the given
            width.
            Note that if you pass only this screen and
            not the match_info_subsurface an error will
            be raised.
        match_info_subsurface: pygame.Surface
            The screen space to draw the match info.
            It will be assumed that PyGame was initialized 
                if this is given.
            If not passed then one will be created.
            It will be half the width of the given
            width.
            Note that if you pass only this screen and
            not the match_info_subsurface an error will
            be raised.
        boards_dir: str = None
            If specified it's the directory the directories
            of PNGs for each board state in each game.
            Else they're stored in a temporary directories
            that is deleted after this object is destroyed.
        frame_dir: str = None
            If specified it's the directory the directories
            of PNGs for each frame that PyGame displays
            for each game.
            Else they're stored in a temporary directories
            that is deleted after this object is destroyed.
            These PNGS are used to make a gif of the
                entire match.
        output_gif: str = None
            If specified the PNG of each frame that PyGame displays is
            turned into a GIF and stored at the specified location.
        win_screen_time: float = 5
            The number of seconds to display win information after the
            entire match.
        initial_pause_time: float=0
            Number of seconds to wait at the start of the match.
        """
        # Setup the super class portion
        super().__init__(white_ai, black_ai, base_timer, wins_required,
                initial_board_state=initial_board_state)

        self._win_screen_time = win_screen_time
        self._first_display = True
        self._initial_pause_time = initial_pause_time
        self._initial_board_state = initial_board_state

        # Initialize PyGame
        if board_subsurface is None and match_info_subsurface\
                is None:
            # If no surfaces are defined we must initialize everything.
            pygame.init()
            self._parent_screen = pygame.display.set_mode(
                    (width, height))
        
            half_width = width / 2
            # Create the sub surfaces
            self._board_subsurface = self._parent_screen.subsurface(
                    pygame.Rect((0,0), (half_width, height)))
            self._match_info_subsurface = self._parent_screen.\
                    subsurface(
                    pygame.Rect((half_width,0), (half_width, height)))
        elif board_subsurface is None or match_info_subsurface is None:
            raise ValueError("Must provide a subsurface for both the board "\
                    " and the match info or neither, not just one.")
        else:
            self._board_subsurface = board_subsurface
            self._match_info_subsurface = match_info_subsurface

        # Initialize the font
        self._font_size = int(self._match_info_subsurface.get_height()/8)
        self._font = pygame.font.SysFont(None, self._font_size)

        # Save the output directory/file names
        self._boards_dir = boards_dir
        self._frames_dir = frames_dir
        self._output_gif = output_gif
        # Setup the output directories
        # Temporary or specified folder for board images?
        if self._boards_dir is not None:
            if os.path.exists(self._boards_dir):
                raise FileExistsError(self._boards_dir)
            else:
                os.mkdir(self._boards_dir)
        else:
            self._boards_dir_handle = tempfile.\
                    TemporaryDirectory(prefix="chesster_boards_")
            self._boards_dir = self._boards_dir_handle.name

        # If the user wants to keep the frames, does the folder already 
        # exist?
        if self._frames_dir is not None:
            if os.path.exists(self._frames_dir):
                raise FileExistsError(self._frames_dir)
            else:
                os.mkdir(self._frames_dir)
        elif self._output_gif is not None:
            self._frames_dir_handle = tempfile.TemporaryDirectory(
                    prefix="chesster_frames_")
            self._frames_dir = self._frames_dir_handle.name

        # Check if the output gif (if specified) already exists
        if self._output_gif is not None:
            if os.path.exists(self._output_gif):
                raise FileExistsError(self._output_gif)

    
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
        self._match_info_subsurface.blit(img, placement)
        

    def _display(self) -> None:
        """This isn't technically required for the object to work
        correctly, but child classes have to at least explicitly set 
        this method to do nothing.
        """
        # Black out the screen
        self._match_info_subsurface.fill((0,0,0))
        # Display text
        match_number = self._record.matches_played + 1
        self._display_text(
            f"Match: {match_number}/"\
            f"{self._record.expected_number_of_match}",
            (self._match_info_subsurface.get_width()*0.01, 0))
        self._display_text(
            f"White Wins: {self._record.white_wins}",
            (self._match_info_subsurface.get_width()*0.01, self._font_size))
        self._display_text(
            f"Black Wins: {self._record.black_wins}",
            (self._match_info_subsurface.get_width()*0.01,
                self._font_size*2))
        self._display_text(
            "Last Game:",
            (self._match_info_subsurface.get_width()*0.01,
                self._font_size*3))
        # Display text
        # Display information about last game
        if len(self._record.game_records) == 0:
            lg_des_p1_text = "N/A"
            lg_des_p2_text = ""
        else:
            if self._record.game_records[-1].result.color:
                color = "White"
            else:
                color = "Black"
            lg_des_p1_text = f"{color} ->"
            lg_des_p2_text = self._record.game_records[-1].result.\
                    short_reason.capitalize()

        self._display_text(
            lg_des_p1_text,
            (self._match_info_subsurface.get_width()*0.01,
                self._font_size*4))
        self._display_text(
            lg_des_p2_text,
            (self._match_info_subsurface.get_width()*0.01,
                self._font_size*5))

        # Match winner info
        if self._record.winner is None:
            match_winner = "N/A"
        else:
            if self._record.game_records[-1].result.color:
                match_winner = "White"
            else:
                match_winner = "Black"
        self._display_text(
            "Match Result:",
            (self._match_info_subsurface.get_width()*0.01,
                self._font_size*6))
        self._display_text(
            match_winner,
            (self._match_info_subsurface.get_width()*0.01,
                self._font_size*7))
       
        # Push finished drawing of screen
        pygame.display.update()

        # Display the empty screen for a bit
        if self._first_display:
            self._first_display = False
            start_time = time.perf_counter()
            while time.perf_counter() - start_time \
                    < self._initial_pause_time:
                self._display()


    def _create_game(self) -> VisualGame:
        """Create a VisualGame object.

        Returns
        -------
        VisualGame
            The newly created visual game.
        """
        # Prep the directory paths
        match_number = self._record.matches_played + 1
        formatted_match_number = f"{match_number:03}"
        board_dir = os.path.join(self._boards_dir, formatted_match_number)
        if self._frames_dir is not None:
            frame_dir = os.path.join(self._frames_dir,
                    formatted_match_number)
        else:
            frame_dir = None

        return VisualGame(self.white_ai, self.black_ai, 
                self.base_timer, 
                initial_board_state=self._initial_board_state,
                screen=self._board_subsurface, 
                board_dir=board_dir, frame_dir=frame_dir,
                win_screen_time=0, initial_pause_time=0)


    def play_match(self) -> chess.COLORS:
        """Play the match!
        This includes displaying the match as it is played.

        Returns
        -------
        chess.COLORS
            The winner of the match.
        """
        # Have we already played?
        if self._record.winner is None:
            # Play the match
            super().play_match()
            
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
                    for _, dirs, _ in os.walk(self._frames_dir, topdown=False):
                        for f_dir in sorted(dirs):
                            f_dir = os.path.join(self._frames_dir, f_dir)
                            for _, _, files in os.walk(f_dir, topdown=False):
                                for image in sorted(files):
                                    yield PIL.Image.open(os.path.join(
                                        f_dir, image))
                it = frames_iter()
                first = next(it)
                first.save(self._output_gif,
                           save_all=True,
                           append_images=it,
                           duration=10,
                           loop=0)

        # Return the winner
        return self._record.winner

