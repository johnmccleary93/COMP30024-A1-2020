import sys
import json
from search.Token import *
from search.util import print_move, print_boom, print_board

class Game:

    def __init__(self, file):
        with open(file) as file:
            data = json.load(file)
            self.tokens = []
            for token in data['white']:
                self.tokens = self.tokens + [Token("white", (token[1], token[2]))]
            for token in data['black']:
                self.tokens = self.tokens + [Token("black", (token[1], token[2]))]
    
    def return_token(self, coords):
        for token in self.tokens:
            if token.coords == coords:
                return token

    def boom(self, token):
        x = -1
        y = -1
        self.tokens.remove(token)
        while x <= 1:
            while y <= 1:
                boom_loc = (token.coords[0]+x, token.coords[1]+y)
                for ind_token in self.tokens:
                    if ind_token.coords == boom_loc:
                        self.boom(self.return_token((token.coords[0]+x, token.coords[1]+y)))
                y += 1
            y = -1
            x += 1
    
    # def is_valid_move(self, token, new_coords):
    #     if (abs(token.coords[0] - new_coords[0]) + abs(token.coords[1] - new_coords[1])) <= token.size and new_coords[0] >= 0 and new_coords[0] <= 7 and new_coords[1] >= 0 and new_coords[1] <= 7:
    #         return True
    #     return False

    def print_tokens(self):
        token_dict = {}
        for token in self.tokens:
            token_key = token.coords
            if token.color == 'white':
                token_value = 'w' + str(token.size)
                token_dict[token_key] = token_value
            else:
                token_value = 'b' + str(token.size)
                token_dict[token_key] = token_value
        print_board(token_dict)


def main():
    return x
    # TODO: find and print winning action sequence
    
if __name__ == '__main__':
    #main()
    game = Game(sys.argv[1])
