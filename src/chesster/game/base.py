"""The base game for Chesster"""
import abc
import chess
import copy
import multiprocessing as mp

from ..ai.base import BaseAI
from ..records import GameResult
from ..timer.base import BaseTimer


class IllegalMove(Exception):
    def __init__(self, board: chess.Board, move: chess.Move):
        """An exception for illegal moves.

        Parameters
        ----------
        board: chess.Board
            The board the move was attempted on.
        move: chess.Move
            The move that was attempted.
        """
        self.board = board
        self.move = move


    @property
    def offending_color(self) -> chess.Color:
        """The color that made the illegal move"""
        return self.board.color


    @property
    def offending_color_name(self) -> str:
        """The name of the color that made the illegal move"""
        return 'White' if self.offending_color == chess.WHITE else 'Black'


    def __str__(self) -> str:
        return f"{self.offending_color_name} attempted illegal move "\
            f"{self.move.uci()} in board:\n{self.board.fen()}"


class BaseGame(abc.ABC):
    def __init__(self, white_ai:BaseAI, black_ai:BaseAI, 
            base_timer:BaseTimer) -> None:
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
        """
        # Save the AI
        self.white_ai = white_ai
        self.black_ai = black_ai

        # Make the timers
        self.white_timer = copy.copy(base_timer)
        self.black_timer = copy.copy(base_timer)

        # Make the board
        self._board = chess.Board()

        # Null out the result
        self._result = None
        
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
    def result(self) -> GameResult:
        """The result of the game.
        If the game has yet to be played, it will be played first.

        Returns
        -------
        GameResult
            The result of the game.
        """
        if self._result is None:
            self.play_game()
        return self._result


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
        if self._result is not None:
            # Yes, so simply return the result
            return self._result

        # Display start of game
        self._display()
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
                # There is a process, is it complete?
                elif self._queue.full():
                    # Stop the timer
                    if self._board.turn == chess.WHITE:
                        self.white_timer.stop()
                    else:
                        self.black_timer.stop()

                    # Remove the move from the queue
                    move = self._queue.get()

                    # Delete the previous AI process
                    self._ai_thread = None

                    # Check that the move is valid
                    if not self._board.is_legal(move):
                        raise IllegalMove(self._board, move)

                    # Make the move
                    self._board.push(move)
                   
                # Regardless, display information
                self._display()
        except IllegalMove as illegal_move:
            # If an AI makes an illegal move, their opponent wins
            self._result = GameResult(self._board, self.white_timer,
                    self.black_timer, illegal_move)
            return self._result

        # The game has ended, record the result, and return it.
        self._result = GameResult(self._board, self.white_timer,
                self.black_timer)
        # Display final result of game.
        self._display()
        return self._result


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

