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
            tokens = tokens + [Token("white", (token[1], token[2]))]
        for token in data['black']:
            tokens = tokens + [Token("black", (token[1], token[2]))]
    return tokens

def main():
    return x
    # TODO: find and print winning action sequence
    
if __name__ == '__main__':
    #main()
    tokens = parse_file(sys.argv[1])
    game = Game(tokens)
    i = 0
    while i < 5:
        game.print_tokens()
        move = game.min_max(game.find_all_moves())
        print(move)
        if move[1] != ():
            game.apply_action(move[1][0], move[1][1])
        i += 1
    