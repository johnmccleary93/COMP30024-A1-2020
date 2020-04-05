import sys
import json
from search.Token import *
from search.Game import *
from search.util import print_move, print_boom, print_board

def parse_file(file):
    with open(file) as file:
        data = json.load(file)
        tokens = []
        for token in data['white']:
            tokens = tokens + [Token("white", (token[1], token[2]), token[0])]
        for token in data['black']:
            tokens = tokens + [Token("black", (token[1], token[2]), token[0])]
    return tokens

def main():
    tokens = parse_file(sys.argv[1])
    game = Game(tokens)
    i = 0
    while i < 3:
        #game.print_tokens()
        move = game.min_max(game.find_all_moves()) #move[0] is the score, move[1] is the token, and place to move, move[2] is the location for it to move and the number of tokens to move
        if move[1] != ():
            if (move[1][0].coords[0] == move[1][1][0][0]) and (move[1][0].coords[1] == move[1][1][0][1]):
                print_boom(move[1][0].coords[0], move[1][0].coords[1])
            else:
                print_move(move[2][0][1], move[1][0].coords[0], move[1][0].coords[1], move[1][1][0][0], move[1][1][0][1])
            game.apply_action(move[1][0], move[1][1])
        i += 1
    # TODO: find and print winning action sequence
    
if __name__ == '__main__':
    main()
    