# Chesster
Purpose is to facilitate custom chess AIs to compete with each other.
Our goal being to have multiple users write their own AI in a Hackathon 
style event to compete at the end.
To facilitate this we need an API class for other to inherit from, as
well as restrictions on the amount of time AI's are allowed to compute.
Of course we also want the ability to view the game as it progresses and
replay past games.
Being able to play against the AI's as a human will also be a great touch.

# Install
Run:
```
pip install .
```
to install from source.

After that you can run `chesster` from the command line.

# Adding an AI
To add an AI create a new file in `src/chesster/ai`.
In it create a class that inherits from `BaseAi`.
Last, add your new AI to `src/chesster/ai/__init__.py`.

