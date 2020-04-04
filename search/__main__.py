import sys
import json
from search.Token import *
from search.Game import *
from search.util import print_move, print_boom, print_board

def parse_file(file):
    with open(file) as file:
        data = json.load(file)
        print(data)
        tokens = []
        for token in data['white']:
            tokens = tokens + [Token("white", (token[1], token[2]), token[0])] #class
        for token in data['black']:
            tokens = tokens + [Token("black", (token[1], token[2]), token[0])]
    return tokens

def main():
    tokens = parse_file(sys.argv[1])
    game = Game(tokens)
    #game.print_tokens()
    game.min_max(game.find_all_moves())
    #game.move_to_coord(tokens[0],(3,5))
        #print(best_best_value)
    # TODO: find and print winning action sequence
    
if __name__ == '__main__':
    main()


#improve the heuristic
#how to move 2 as well maybe put it in **find moves?? w all that use it need to be updated

# w tazkar kenet dalla truh left w right w i might need to 