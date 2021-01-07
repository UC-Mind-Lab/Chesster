import chess
import random
random.seed()

from .base import BaseAI
from ..timer.base import BaseTimer

import numpy as np
import tensorflow as tf

def board_to_bitboard(fen):
    bitboard_dict = {
        "P": [],
        "R": [],
        "N": [],
        "B": [],
        "Q": [],
        "K": [],
        "p": [],
        "r": [],
        "n": [],
        "b": [],
        "q": [],
        "k": []
    }
    fields = fen.split(" ")
    placement = fields[0].split("/")

    y = 0
    while y < 8:
        x = 0
        n = 0
        while x < 8:
            # print(y, x, placement[y])
            if placement[y][n].isnumeric():
                for i in range(int(placement[y][n])):
                    for key in bitboard_dict.keys():
                        bitboard_dict[key].append(0)
                x += int(placement[y][n])
            else:
                for key in bitboard_dict.keys():
                    bitboard_dict[key].append(0)
                bitboard_dict[placement[y][n]][8*y + x] = 1
                x += 1
            n += 1
        y += 1

    bitboard = []
    for key in bitboard_dict:
        for bit in bitboard_dict[key]:
            bitboard.append(bit)

    return bitboard

letters = ["a","b","c","d","e","f","g","h"]
numbers = ["1","2","3","4","5","6","7","8"]

def get_top(l, n):
    top = []
    for i in range(n):
        top.append((max(l), l.index(max(l))))
        l[l.index(max(l))] = 0
    return top

class Jeffbot(BaseAI):
    def make_move(self, board:chess.Board, timer:BaseTimer) -> chess.Move:
        model = tf.keras.models.load_model("./src/chesster/ai/models/jeffbot")
        bitboard = board_to_bitboard(board.fen())

        x = np.array([bitboard])
        x = x.reshape(x.shape[0], x.shape[1], 1).astype(float)

        predictions = list(model.predict(x)[0])
        predictions_separated = [
            predictions[:7],
            predictions[8:15],
            predictions[16:23],
            predictions[24:31]
        ]

        n = 4

        predictions_top = [
            get_top(predictions_separated[0], n),
            get_top(predictions_separated[1], n),
            get_top(predictions_separated[2], n),
            get_top(predictions_separated[3], n)
        ]

        print(predictions_top)

        move = None
        found_move = False

        moves = []

        for index, value in enumerate(board.legal_moves):
            moves.append(value)

        for i in range(4):
            for j in range(4):
                for k in range(4):
                    for l in range(4):
                        move = letters[ predictions_top[0][i][1] ] + \
                            numbers[ predictions_top[1][j][1] ] + \
                            letters[ predictions_top[2][k][1] ] + \
                            numbers[ predictions_top[3][l][1] ]

                        # print("trying " + str(move))
                        try: 
                            move = chess.Move.from_uci(move)
                        except:
                            print("illegal :(")

                        if move in moves:
                            print("move " + str(move) + " in moves")
                            found_move = True
                            break

                    else:
                        continue
                    break
                else:
                    continue
                break
            else:
                continue
            break


        # letter0 = letters[predictions_separated[0].index(max(predictions_separated[0]))]
        # number0 = numbers[predictions_separated[1].index(max(predictions_separated[1]))]
        # letter1 = letters[predictions_separated[2].index(max(predictions_separated[2]))]
        # number1 = numbers[predictions_separated[3].index(max(predictions_separated[3]))]

        # move = chess.Move.from_uci(letter0 + number0 + letter1 + number1)
        # print(letter0 + number0 + letter1 + number1)

        # moves = []
        # for index, value in enumerate(board.legal_moves):
        #     moves.append(value)
        # print()
        # print(moves)
        # print(type(moves[0]))
        # print(move in moves)
        # print()

        print(move)

        return move if found_move else random.choice(list(board.legal_moves))
