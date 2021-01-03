# Chesster
This provides a standard for a Chess AI hackathon and a graphical display of matches.

# Participation
## Installation
To participate you must clone this repository through git, and create a branch (off of the development branch)
```
git checkout development
git checkout -b YourName
```

Before you start coding you should ensure that Chesster runs on your system via installing it and it's
dependencies.
```
pip install .
```
After that you will have the `chesster` command available on your system.
Try it out by running:
```
chesster RandomAI RandomAI
```
This will start a single game match between two instances of the RandomAI.

To try your hand at playing against the `RandomAI` try running:
```
chesster RandomAI Human
```

To see all of the options that chesster has availabe to you run:
```
chesster -h
```

# Adding an AI
AIs in chesster are all a child class of `BaseAi` which is defined in `src/chesster/ai/base.py`.
Creating your own would be easily accomplished by copying the implementation of `RandomAi` which
is defined in `src/chesster/ai/random.py`.
Note that you will need to change the name of the class witn the copied file, and a few of the
documentation strings.
Finally, add your new class to the `AI` dictionary within `src/chesster/ai/__init__.py`.

To test out that your new copy of the `RandomAI` works as intended you can do so in one of
two ways:
+ Reinstall Chesster with `pip install .`, and run the `chesster` command.
+ Run the `src/chesster/cli/__init__.py` file directly
  + This will be easier to use within a fancy IDE like PyCharm.
After it works as expected you'll be free to build your AI as you see fit!
The requirements for your AI are simple and are in the `make_move` method.
Firstly your AI must be able to make descions based on only two pieces of information
+ board: A [Board object from the chess python library](https://python-chess.readthedocs.io/en/latest/core.html#board)
  + This object contains the information about the current board state and previous moves.
  + Hint: `board.turn` will tell your AI it's color
  + Hint: `board.legal_moves` will tell you all the possible legal moves. If your AI attempts to make an illegal move it will lose!
  + Hint: You can attempt to modify the board object but that won't actually do anything as your AI is only given a copy of the board object.
+ timer: A [custom Timer object within Chesster](src/chesster/timer/base.py)
  + Hint: There are several types of timers, but you're likely only interested in the `timer.seconds_left` property
  + Hint: You can attempt to stop the timer with `timer.stop()`, but that won't actually do anything as your AI is only given a copy
  of the timer object.
Finally, your AI must return a single object: [chess.Move](https://python-chess.readthedocs.io/en/latest/core.html#moves). (Remember that if your AI submits an illegal move it loses).

# How to Teach your AI
How you implement your AI's learning will likely be very different from everyone else, but your best start is the information in the [JSON](https://docs.python.org/3/library/json.html) output that chesster creates of each match.
By default Chesster will not save it, so be sure to specifiy it!
To do so on the command line run:
```
chesster RandomAI RandomAI --record_file record.json
```
The resulting file is dense with information as it knows the board state of every move that took place in the game!
The best way to understand it is to look at the [MatchRecord](src/chesster/records/match.py) object, specifically the `to_dict` method.
In Python JSON object are basically just dictionaries so each object within the [records module](src/chesster/records) has a `to_dict` and `from_dict` method.
Note that [MatchRecord](src/chesster/records/match.py) keeps track of the number of wins required in a match, the number of wins each color got and a list of
[GameRecord](src/chesster/records/game.py) objects.
Each of the [GameRecord](src/chesster/records/game.py) objects knows what AI each color was, the initial board state, the eventual [GameResult](src/chesster/records/result.py) and a list of each [Move](src/chesster/records/move.py).
From this information you should be able to teach your AI how to play chess, as well as debug what happens during a game.

