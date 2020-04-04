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

    def __init__(self, tokens):
        self.tokens = tokens
    
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

    def move_to_coord(self, token, best_coord):
        self.print_tokens()
        new_coords = []
        new_coords.append(token.coords[0])
        new_coords.append(token.coords[1])
        print(f"The token is at {new_coords}")
        print(f"The token should go to {best_coord}")

        while new_coords[0] < best_coord[0]:
            new_coords[0] += 1
            print_move(token.size,new_coords[0] - 1,new_coords[1],new_coords[0],new_coords[1])
            self.move_token2(token,(tuple(new_coords),1))
            self.print_tokens()

        while new_coords[0] > best_coord[0]:
            new_coords[0] -= 1
            print_move(token.size,new_coords[0] + 1,new_coords[1],new_coords[0],new_coords[1])
            self.move_token2(token,(tuple(new_coords),1))
            self.print_tokens()

        while new_coords[1] < best_coord[1]:
            new_coords[1] += 1
            print_move(token.size,new_coords[0],new_coords[1]-1,new_coords[0],new_coords[1])
            self.move_token2(token,(tuple(new_coords),1))
            self.print_tokens()

        while new_coords[1] > best_coord[1]:
            new_coords[1] -= 1
            print_move(token.size,new_coords[0],new_coords[1]+1,new_coords[0],new_coords[1])
            self.move_token2(token,(tuple(new_coords),1))
            self.print_tokens()

        if (new_coords[0] == best_coord[0]) and (new_coords[1] == best_coord[1]):
            self.boom(token)
            print_boom(token.coords[0],token.coords[1])
            self.print_tokens()
            pass


    def best_score_for_token(self,token,actions, depth=32):

        best_value = -1000
        best_move = ()

        if depth == 0:
            return (best_value,best_move)

        for action in actions:
            new_board = Game(copy.deepcopy(self.tokens))
            token1 = new_board.return_token(token.coords)
            if token1 != None:
                new_board.apply_action(token1, action)
                token1_coords = token1.coords
                token1_size = token1.size
                token1_tuple = (token1_coords,token1_size)
                if not (token1_tuple in Game.list_tokens):   
                    Game.list_tokens.append(token1_tuple)
                    best_value_move = new_board.best_score_for_token(token1,new_board.find_moves(token1),depth-1)
                    max_value = max(new_board.board_score(),best_value_move[0])
                else:
                    max_value = new_board.board_score()
            #if boom
            if token1 == None:
                max_value = new_board.board_score()

            if max_value > best_value:
                #print(f"{max_value} if men ruh honeek {action}")
                best_value = max_value
                best_move = action
                if Game.best_best_value < max_value:
                            Game.best_best_value = max_value
                            print(Game.best_best_value)
                            Game.best_best_coord = list(token.coords)
                            print(Game.best_best_coord)

        return (best_value, best_move)


    def min_max(self, moves): #moves hon hiye dictionary find all moves

        #check the the highest score for every tuple, then move the tuple with the highest score to the desired location, then reevaluate the situation again
        while moves:
            for token in moves.keys():
                print(token.coords)
                self.best_score_for_token(token,moves[token])
                Game.best_coord_dict[token] = (Game.best_best_coord,Game.best_best_value)
                Game.best_best_coord = []
                Game.best_best_value = - 1000
                Game.list_tokens = []
            print(Game.best_coord_dict)


            max1 = -1000
            for token in Game.best_coord_dict:
                if Game.best_coord_dict[token][1] > max1:
                    max1 = Game.best_coord_dict[token][1]
                    max_token = token
                    max_coord = Game.best_coord_dict[token][0]

            self.move_to_coord(max_token,max_coord)
            Game.best_coord_dict = {}
            del moves[max_token]
            print(moves.keys())

        pass

                    

    def apply_action(self, token, action): #action is where its gonna move
        if token.coords == action[0]:
            self.boom(token) 
        else:
            self.move_token2(token, action)  


