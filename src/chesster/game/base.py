"""The base game for Chesster"""
import abc
import chess
import copy
import multiprocessing as mp

from .exceptions import IllegalMove
from ..ai.base import BaseAI
from ..records.game import GameRecord, GameResult, Move
from ..timer.base import BaseTimer


class BaseGame(abc.ABC):
    def __init__(self, white_ai:BaseAI, black_ai:BaseAI, 
            base_timer:BaseTimer, continually_redraw_display:bool,
            initial_board_state:str=None) -> None:
        """The base game object for Chesster.
        Note that it uses multi-threading when running the AI's
        computation of the next move to take. The AI's shouldn't
        really be aware of that though, as they don't need to
        communicate across threads, this object does that for
        them.

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
        continually_redraw_display: bool
            Rather the state of the game should be continually redrawn
            while waiting for an AI to make a move. This makes sense
            for graphical outputs or smart terminal outputs like the
            curses library. Not so much for simple print statements.
        """
        # Save the AI
        self.white_ai = white_ai
        self.black_ai = black_ai

        # Make the timers
        self.white_timer = copy.copy(base_timer)
        self.black_timer = copy.copy(base_timer)

        # Make the board
        if initial_board_state:
            self._board = chess.Board(fen=initial_board_state)
        else:
            self._board = chess.Board()

        # Save continually_redraw_display
        self._continually_redraw_display = continually_redraw_display

        # Make an empty Game record
        self._record = GameRecord(self._board, 
                self.white_ai.__class__.__name__,
                self.black_ai.__class__.__name__
                )
        
        # Multi-threading stuff
        self._queue = mp.Queue(maxsize=1)
        self._ai_thread = None


    @abc.abstractmethod
    def _display(self) -> None:
        """This isn't technically required for the object to work
        correctly, but child classes have to at least explicitly set 
        this method to do nothing.
        """
        ...


    @property
    def record(self) -> GameRecord:
        """The result of the game.
        If the game has yet to be played, it will be played first.

        Returns
        -------
        GameRecord
            The record of the game.
        """
        if self._record.result is None:
            self.play_game()
        return self._record


    @property
    def result(self) -> GameResult:
        """The result of the game.
        If the game has yet to be played, it will be played first.

        Returns
        -------
        GameResult
            The result of the game.
        """
        if self._record.result is None:
            self.play_game()
        return self._record.result


    @property
    def _game_alive(self) -> bool:
        """Rather the board is still valid and timers are running.

        Returns
        -------
        bool
            Rather the game is still afoot.
        """
        return not self._board.is_game_over() and \
                self.white_timer.alive and self.black_timer.alive


    def play_game(self) -> GameResult:
        """Play the game!
        This includes displaying the game as it is played.

        Returns
        -------
        GameResult
            The result of the game. It's also saved to self._result
        """
        # Have we already played?
        if self._record.result is not None:
            # Yes, so simply return the result
            return self._record.result

        # Play the game!
        try:
            while self._game_alive:
                # Is there a process running to calculate a move?
                if self._ai_thread is None:
                    # There is not, so we need to start one
                    if self._board.turn == chess.WHITE:
                        self.white_timer.start()
                        self._ai_thread = mp.Process(
                                target=self._ai_thread_method,
                                args=(self._queue, self._board,
                                    self.white_ai, self.white_timer))
                    else:
                        self.black_timer.start()
                        self._ai_thread = mp.Process(
                                target=self._ai_thread_method,
                                args=(self._queue, self._board,
                                    self.black_ai, self.black_timer))
                    self._ai_thread.start()

                    # Display updated board
                    self._display()

                # There is a process, is it complete?
                elif self._queue.full():
                    # Stop the timer
                    if self._board.turn == chess.WHITE:
                        time_used = self.white_timer.stop()
                    else:
                        time_used = self.black_timer.stop()

                    # Remove the move from the queue
                    move = self._queue.get()

                    # Delete the previous AI process
                    self._ai_thread = None

                    # Check that the move is valid
                    if not self._board.is_legal(move):
                        # Note that the recorded illegal move does not change
                        # the board state.
                        self._record.append(
                                Move(move, self._board.turn,
                                    time_used, self._board))
                        raise IllegalMove(self._board, move)

                    # Make the move
                    self._board.push(move)

                    # Record the move
                    # The turn color is "not"ed as the pushing of the move 
                    # flips the turn to the other player.
                    self._record.append(
                            Move(move, not self._board.turn,
                                time_used, self._board))

                    # Redraw updated board
                    if self._continually_redraw_display:
                        self._display()

                # If nothing else, just redraw the display
                elif self._continually_redraw_display:
                    self._display()
                # We don't want to continually redraw the display, so let's wait
                else:
                    self._ai_thread.join()

                   
        except IllegalMove as illegal_move:
            # If an AI makes an illegal move, their opponent wins
            self._record.result = GameResult(self._board, 
                    self.white_timer, self.black_timer, illegal_move)
            return self._record.result

        # The game has ended, record the result, and return it.
        self._record.result = GameResult(self._board, self.white_timer,
                self.black_timer)
        # Display final result of game.
        self._display()
        return self._record.result


    @staticmethod
    def _ai_thread_method(queue:mp.Queue, board:chess.Board, ai:'BaseAi', 
            timer:'BaseTimer') -> None:
        """Actions for an AI thread to perform. 
        This static method is for use in starting a new thread and
        saves the move to the queue object.

        Parameters
        ---------- 
        queue: multiprocessing.Queue 
            The queue to push the calculated move to.
        board: chess.Board
            The board the AI will be calculating a move upon.
        ai: chesster.ai.base.BaseAI
            A Chesster AI that will calculate a move.
        timer: chesster.timer.base.BaseTimer
            The timer associated with the AI
        """
        # Calculate the move
        move = ai.make_move(board, timer)
        # Put the move into the queue
        queue.put(move)

