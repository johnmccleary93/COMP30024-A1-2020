import sys
import json
from search.Token import *
from search.util import print_move, print_boom, print_board
import pdb
import copy

class Game:

    def __init__(self, tokens, moves_taken=[]):
        self.tokens = tokens
        self.moves_taken = moves_taken

        
    
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

    #Assumes board size is 7. Find all moves for a given token.
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
        moves2 = []
        count = 1
        for move in moves:
            while count <= token.size:
                moves2 = moves2 + [(move,count)]
                count += 1
            count = 1
        moves2 = list(set(moves2))
        return moves2
    
    def move_token(self, token, new_coords, size):
        if self.return_token(new_coords) is not None:
            self.return_token(new_coords).size += size
        else:
            self.tokens = self.tokens + [Token(token.color, new_coords, size)]
        token.size -= size
        if token.size == 0:
            self.tokens.remove(token)

    def count_valid_moves(self, color):
        count = 0
        for token in self.tokens:
            if token.color == color:
                count += len(self.find_moves(token))
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
    
    #Find all moves for a given color, by default white. Needs to account for size to move.
    def find_all_moves(self, color='white'):
        all_valid_moves = {}
        for token in self.tokens:
            if token.color == color:
                all_valid_moves[token] = self.find_moves(token) 
        return all_valid_moves
    

    #Assumes player is white
    def board_score(self):
        score = 0
        for token in self.tokens:
            if token.color == 'black':
                score -= 2
            score = score + len(self.find_all_moves().values()) - len(self.find_all_moves('black').values())
        return score

    def min_max(self, moves, depth=8):
        best_value = self.board_score()
        best_move = ()
        best_moves = self.moves_taken
        if depth == 0 or moves == {} or best_value >= 0:
            return (best_value, best_move, best_moves)
        else:
            for token in moves.keys():
                for action in moves[token]:
                    new_board = Game(copy.deepcopy(self.tokens), self.moves_taken + [(token,action)])
                    new_board.apply_action(new_board.return_token(token.coords), action)
                    new_value = new_board.min_max(new_board.find_all_moves(), depth-1)
                    if new_value[0] >= 0:
                        best_value = new_value[0]
                        best_moves = new_value[2]
                        best_move = (token, action)
                        return (best_value, best_move, best_moves)
                    elif new_value[0] > best_value or (new_value[0] == best_value and len(new_value[2]) < len(best_moves)):
                        best_value = new_value[0]
                        best_moves = new_value[2]
                        best_move = (token, action)
            return (best_value, best_move, best_moves)               

    def apply_action(self, token, action):
        if token.coords == action[0]:
            self.boom(token) 
        else:
            self.move_token(token, action[0], action[1])   

