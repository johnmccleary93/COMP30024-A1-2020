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

    #Assumes board size is 7.
    def find_moves(self, token):
        moves = [token.coords]
        count = 1
        while count <= token.size:
            moves = moves + [(max(token.coords[0]-count, 0), token.coords[1])]
            moves = moves + [(min(token.coords[0]+count, 7), token.coords[1])]
            moves = moves + [(token.coords[0], max(token.coords[1]-count, 0))]
            moves = moves + [(token.coords[0], min(token.coords[1]+count, 7))]
            count += 1
        moves = list(set(moves))
        moves = [move for move in moves if self.return_token(move) is None or self.return_token(move).color == token.color]
        print(moves)
        return moves
    
    def move_token(self, token, new_coords):
        distance = abs(token.coords[0] - new_coords[0]) + abs(token.coords[1] - new_coords[1])
        if self.return_token(new_coords) is not None:
            self.return_token(new_coords).size += distance
        else:
            self.tokens = self.tokens + [Token(token.color, new_coords, size=distance)]
        if distance == token.size:
            self.tokens.remove(token)
        else:
            token.size -= distance

    def count_valid_moves(self, color):
        count = 0
        for token in self.tokens:
            if token.color == color:
                count += len(self.find_moves(token))
        print(count)
        return count

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
    game.print_tokens()
    game.move_token(game.tokens[5], (6,3))
    game.print_tokens()
    game.move_token(game.tokens[5], (6,2))
    game.print_tokens()