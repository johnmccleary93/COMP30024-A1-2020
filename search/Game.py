import sys
import json
from search.Token import *
from search.util import print_move, print_boom, print_board #search is the folder and util is the file
import pdb
import copy
import time

class Game:

    best_best_value = -1000
    best_best_coord = []
    best_coord_dict = {}
    list_tokens = []

    def __init__(self, tokens, moves_taken=[]):
        self.tokens = tokens
        self.moves_taken = moves_taken
    
    def return_token(self, coords):
        for token in self.tokens:
            if token.coords == coords:
                return token

    def boom(self, token):
        x = -1 #increment them to blow up everything
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
        moves = [token.coords] #same coordinates in case blows up
        count = 1
        while count <= token.size:
            moves = moves + [(max(token.coords[0]-count, 0), token.coords[1])]
            moves = moves + [(min(token.coords[0]+count, 7), token.coords[1])]
            moves = moves + [(token.coords[0], max(token.coords[1]-count, 0))] #min and max kermel iza negative w se3ta byetla3 fi duplicates
            moves = moves + [(token.coords[0], min(token.coords[1]+count, 7))]
            count += 1
        moves = list(set(moves)) #a way to remove all duplicates
        moves = [move for move in moves if self.return_token(move) is None or self.return_token(move).color == token.color] #removes coordinates that it cannot physically step into because of the other color
        moves2 = []

        count = 1
        for move in moves:
            while count <= token.size:
                moves2 = moves2 + [(move,count)]
                count += 1
            count = 1

        #remove duplicates at the beginning
        count = 1
        while count < token.size:
            moves2.pop(0)
            count += 1

        return moves2
    
    def move_token(self, token, new_coords): #No need la size ma sah?
        if self.return_token(new_coords) is not None:
            self.return_token(new_coords).size += size #if there is a token of the same color there, then you add the size
            #otherwise create new token and add it to tokens and remove the other one
        else:
            self.tokens = self.tokens + [Token(token.color, new_coords, size)]
        token.size -= size
        if token.size == 0:
            self.tokens.remove(token)

            #number of valid moves for all the tokens of the same color combined
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
    def find_all_moves(self, color='white'): #returns a dict with the token as the key, and list of moves of values
        all_valid_moves = {}
        for token in self.tokens:
            if token.color == color:
                all_valid_moves[token] = self.find_moves(token)  #[key] = values
        return all_valid_moves
    

       #Assumes player is white
    def board_score(self):
        score = 0
        for token in self.tokens:
            if token.color == 'black':
                score -= 1 #heydi betkhali score yzeed iza fejarna wahdi
            if token.color == 'white':
                score += 0.5
       # print(score)
        return score


    def move_token2(self, token, new_coords_size):
        if token.size > new_coords_size[1]:
            #print("true")
            #print(f"token size is {token.size} while size to move is {new_coords_size[1]}")
            temp_size = token.size
            temp_coords = token.coords
            if self.return_token(new_coords_size[0]) is not None:
                token.size = self.return_token(new_coords_size[0]).size + new_coords_size[1]  
                self.tokens.remove(self.return_token(new_coords_size[0]))
                token.coords = new_coords_size[0]
                self.tokens = self.tokens + [Token(token.color, temp_coords, temp_size)]
            else:
                token.size = new_coords_size[1]
                token.coords = new_coords_size[0]
                self.tokens = self.tokens + [Token(token.color, temp_coords, temp_size - new_coords_size[1])] 

        else:
            if self.return_token(new_coords_size[0]) is not None:
                #print(new_coords_size[0])
                #print(token.coords)
                #print("true2")
                token.size += self.return_token(new_coords_size[0]).size #if there is a token of the same color there, then you add the size
                self.tokens.remove(self.return_token(new_coords_size[0]))
            token.coords = new_coords_size[0]
        pass


    def move_to_coord(self, token, best_moves):
        self.print_tokens()

        print(f"The token is at {token.coords}")
        print(f"The token should go to {best_moves[-1]}")
        last_move = best_moves[-1]

        for move in best_moves:

            print_move(move[1],token.coords[0],token.coords[1],move[0][0],move[0][1])
            self.move_token2(token,move)
            print(move)
            self.print_tokens()

        self.boom(token)
        print_boom(token.coords[0],token.coords[1])
        self.print_tokens()

        pass


    def best_score_for_token(self,token,actions, depth=100):

        best_value = self.board_score()
        best_move = ()
        best_moves = self.moves_taken
        flag = 0

        if depth == 0:
            return (best_value,best_move,best_moves)

        for action in actions:
            new_board = Game(copy.deepcopy(self.tokens), self.moves_taken + [action])
            token1 = new_board.return_token(token.coords)
            if token1 != None:
                new_board.apply_action(token1, action)
                token1_coords = token1.coords
                token1_size = token1.size
                token1_tuple = (token1_coords,token1_size)
                if not (token1_tuple in Game.list_tokens):   
                    Game.list_tokens.append(token1_tuple)
                    best_value_move = new_board.best_score_for_token(token1,new_board.find_moves(token1),depth-1)
                    max_value = best_value_move[0]
                    flag = 1
                else:
                    max_value = new_board.board_score()

            #if boom
            if token1 == None:
                max_value = new_board.board_score()

            if flag == 1 and ((max_value > best_value) or (max_value == best_value and len(best_value_move[2]) < len(best_moves))):
                best_value = max_value
                best_move = action
                best_moves = best_value_move[2]
                #print(best_moves)
                if max_value == best_value and len(best_value_move[2]) < len(best_moves):
                    if Game.best_best_value < max_value:
                            Game.best_best_value = max_value
                            print(Game.best_best_value)
                            Game.best_best_coord = list(token.coords)
                            print(Game.best_best_coord)
                flag = 0

            elif max_value > best_value:
                #print(f"{max_value} if men ruh honeek {action}")
                best_value = max_value
                best_move = action
                if Game.best_best_value < max_value:
                            Game.best_best_value = max_value
                            print(Game.best_best_value)
                            Game.best_best_coord = list(token.coords)
                            print(Game.best_best_coord)

        return (best_value, best_move, best_moves)


    def min_max(self, moves): #moves hon hiye dictionary find all moves

        #check the the highest score for every tuple, then move the tuple with the highest score to the desired location, then reevaluate the situation again
        while moves:
            for token in moves.keys():
                print(token.coords)
                list_moves = self.best_score_for_token(token,moves[token])
                #print(list_moves[2])
                Game.best_coord_dict[token] = (Game.best_best_coord,Game.best_best_value,list_moves[2])
                Game.best_best_coord = []
                Game.best_best_value = - 1000
                Game.list_tokens = []
            print(Game.best_coord_dict)


            max1 = -1000
            for token in Game.best_coord_dict:
                if Game.best_coord_dict[token][1] > max1:
                    max1 = Game.best_coord_dict[token][1]
                    max_token = token
                    best_moves = Game.best_coord_dict[token][2]

            self.move_to_coord(max_token,best_moves)
            Game.best_coord_dict = {}
            #del moves[max_token]
            moves = self.find_all_moves()
            print(moves.keys())

        pass

                    

    def apply_action(self, token, action): #action is where its gonna move
        if token.coords == action[0]:
            self.boom(token) 
        else:
            self.move_token2(token, action)  


