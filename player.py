import sys
import pdb
import copy
import time

class ExamplePlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the 
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your 
        program will play as (White or Black). The value will be one of the 
        strings "white" or "black" correspondingly.
        """
        # TODO: Set up state representation.
        tokens = Game.init_state(self)
        self.game = Game(tokens,colour)



    def action(self):
        """
        This method is called at the beginning of each of your turns to request 
        a choice of action from your program.

        Based on the current state of the game, your player should select and 
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """

        #determine the depth to be used in the alpha beta function
        depth = self.game.proper_depth()

        #Check if we should be aggresive, defensive or neutral
        strategy = self.game.off_def_neutral(self.game.my_color)

        # TODO: Decide what action to take, and return it
        move = self.game.alpha_beta(self.game.find_all_moves(self.game.my_color,strategy), True, self.game.my_color, strategy,depth)

        #this is of the form (token,((x,y),size)) where token is the token to be moved
        # x,y are the destination coordinates, and the size is the number of tokens to be moved
        best_move = move[1] 
        
        token = best_move[0]
        if token.coords == best_move[1][0]: #then we should boom the token
            return ("BOOM",token.coords)
        else:
            return("MOVE",best_move[1][1],token.coords,best_move[1][0])


    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s 
        turns) to inform your player about the most recent action. You should 
        use this opportunity to maintain your internal representation of the 
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (White or Black). The value will be one of the strings "white" or
        "black" correspondingly.

        The parameter action is a representation of the most recent action
        conforming to the spec's instructions for representing actions.

        You may assume that action will always correspond to an allowed action 
        for the player colour (your method does not need to validate the action
        against the game rules).
        """
        # TODO: Update state representation in response to action.

        #Question: These functions work well with both black and white right?
        if action[0] == "BOOM":
            token = self.game.return_token(action[1])
            self.game.boom(token)

        elif action[0] == "MOVE":
            token = self.game.return_token(action[2])
            self.game.move_token(token,action[3],action[1])




class Token:
    def __init__(self, color, coords, size=1):
        self.color = color
        self.coords = coords
        self.size = size #Can we assume that on initialization, will never include a stack


class Game:

    def __init__(self, tokens,my_color,moves_taken=[]):
        self.tokens = tokens
        self.my_color = my_color
        self.moves_taken = moves_taken
        self.current_score = self.board_score()

    
    def init_state(self):
        tokens = []
        tokens = tokens + [Token("white", (0,0),1)]
        tokens = tokens + [Token("white", (0,1),1)]
        tokens = tokens + [Token("white", (1,0),1)]
        tokens = tokens + [Token("white", (1,1),1)]
        tokens = tokens + [Token("white", (3,0),1)]
        tokens = tokens + [Token("white", (3,1),1)]
        tokens = tokens + [Token("white", (4,0),1)]
        tokens = tokens + [Token("white", (4,1),1)]
        tokens = tokens + [Token("white", (6,0),1)]
        tokens = tokens + [Token("white", (6,1),1)]
        tokens = tokens + [Token("white", (7,0),1)]
        tokens = tokens + [Token("white", (7,1),1)]
        tokens = tokens + [Token("black", (0,7),1)]
        tokens = tokens + [Token("black", (1,7),1)]
        tokens = tokens + [Token("black", (0,6),1)]
        tokens = tokens + [Token("black", (1,6),1)]
        tokens = tokens + [Token("black", (3,7),1)]
        tokens = tokens + [Token("black", (4,7),1)]
        tokens = tokens + [Token("black", (3,6),1)]
        tokens = tokens + [Token("black", (4,6),1)]
        tokens = tokens + [Token("black", (6,7),1)]
        tokens = tokens + [Token("black", (7,7),1)]
        tokens = tokens + [Token("black", (6,6),1)]
        tokens = tokens + [Token("black", (7,6),1)]
        return tokens 

    #Neutral if total number of tokens is less than 7
    #Else offensive if our number of tokens is >= than that 
    #of the oppopnets, defensive otherwise
    #Returns -1 for neurtal, 1 for offensive, 0 for defensive
    def off_def_neutral(self,my_color):
        o = 0;
        d = 0;

        if self.num_of_tokens() <= 7:
            return "neutral"

        for token in self.tokens:
            if token.color == my_color:
                o += token.size
            else:
                d += token.size
        if o > d:
            return "aggressive"
        else:
            return "defensive"

    #Returns the depth to be used in the alpha beta function
    #Depth is chosen according to the number of tokens in the game
    #The greater the number of tokens, the smaller the depth
    def proper_depth(self):
        sum = self.num_of_tokens()

        if sum >= 20:
            return 2
        elif sum > 15:
            return 3
        elif sum > 10:
            return 4
        else:
            return 6

    #Returns the total number of tokens on the board
    def num_of_tokens(self):
        sum = 0
        for token in self.tokens:
            sum += token.size
        return sum

    #Returns the enemy's color
    def opp_color(self,my_color):
        if my_color == "white":
            return "black"
        return "white"
    
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
                    new_value = new_board.alpha_beta(new_board.find_all_moves(self.opp_color(player_color), mode), False, player_color, mode, depth-1, alpha, beta)
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
                    new_value = new_board.alpha_beta(new_board.find_all_moves(player_color,mode), True, player_color, mode, depth-1, alpha, beta)
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
