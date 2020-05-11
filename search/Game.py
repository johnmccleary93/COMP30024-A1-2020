import sys
import json
from search.Token import *
from search.util import print_move, print_boom, print_board
import pdb
import copy
import time

class Game:

    def __init__(self, tokens, moves_taken=[]):
        self.tokens = tokens
        self.moves_taken = moves_taken
        self.current_score = self.board_score()

        
    
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
        if token.color == 'white':
            return 1
        else:
            return 0


    #Assumes board size is 7. Find all moves for a given token.
    def find_moves(self, token, mode="neutral"):
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
        if mode == "aggressive":
            moves2 = [move for move in moves2 if self.aggressive_move(token, move)]
        elif mode == "defensive":
            moves2 = [move for move in moves2 if self.defensive_move(token, move)]
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
    def find_all_moves(self, color='white', mode="neutral"):
        all_valid_moves = {}
        for token in self.tokens:
            if token.color == color:
                all_valid_moves[token] = self.find_moves(token, mode) 
        return all_valid_moves
    
    #Assumes player is white
    def board_score(self, player="white"):
        score = 0
        for token in self.tokens:
            if token.color != player:
                score -= 2
            score = score + len(self.find_all_moves(mode="neutral").values()) - len(self.find_all_moves('black', mode="neutral").values())
        return score
        
    def token_dists(self, token, color):
        dist = 0
        for each_token in self.tokens:
            if each_token.color == color:
                dist += abs(token.coords[0] - each_token.coords[0]) + abs(token.coords[1] - each_token.coords[1])
        return dist

    def aggressive_move(self, token, action):
        if token.coords == action[0]:
            return True
        if token.color == "white":
            if action[0][1] >= token.coords[1]:
                return True
            else: 
                return False
        else:
            if action[0][1] <= token.coords[1]:
                return True
            else:
                return False

    def defensive_move(self, token, action):
        if token.coords == action[0]:
            return True
        orig_dist = self.token_dists(token, token.color)
        new_board = Game(copy.deepcopy(self.tokens), self.moves_taken + [(token,action)])
        new_board.apply_action(new_board.return_token(token.coords), action)
        new_dist = new_board.token_dists(new_board.return_token(action[0]), token.color)
        if new_dist > orig_dist:
            return True
        else:
            return False

    def alpha_beta(self, moves, maximizingPlayer, player_color, mode, depth=3, alpha=-100000, beta=100000): #Add depth and new value updates
        best_move = ()
        best_moves = self.moves_taken
        if depth == 0 or moves == {}:
            return (self.board_score(player_color), best_move, best_moves)
        #breakpoint()
        if maximizingPlayer:
            value = - 100000
            for token in moves.keys():
                for action in moves[token]:
                    new_board = Game(copy.deepcopy(self.tokens), self.moves_taken + [(token,action)])
                    new_board.apply_action(new_board.return_token(token.coords), action)
                    new_value = new_board.alpha_beta(new_board.find_all_moves("black", mode), False, "white", mode, depth-1, alpha, beta)
                    if new_value[0] > value or (new_value[0] == value and len(new_value[2]) < len(best_moves)):
                        value = new_value[0]
                        best_moves = new_value[2]
                        best_move = (token, action)
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        return (value, best_move, best_moves)
            return (value, best_move, best_moves)
        else:
            value = 100000
            for token in moves.keys():
                for action in moves[token]:
                    new_board = Game(copy.deepcopy(self.tokens), self.moves_taken + [(token,action)])
                    new_board.apply_action(new_board.return_token(token.coords), action)
                    new_value = new_board.alpha_beta(new_board.find_all_moves("white",mode), True, "white", mode, depth-1, alpha, beta)
                    if new_value[0] < value or (new_value[0] == value and len(new_value[2]) < len(best_moves)):
                        value = new_value[0]
                        best_moves = new_value[2]
                        best_move = (token, action)
                    beta = min(beta, value)
                    if alpha >= beta:
                        return (value, best_move, best_moves)
            return (value, best_move, best_moves)
            

    def apply_action(self, token, action):
        if token.coords == action[0]:
            self.boom(token) 
        else:
            self.move_token(token, action[0], action[1])   

