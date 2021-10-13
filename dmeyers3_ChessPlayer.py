from types import new_class
from typing import Counter
from chess_player import ChessPlayer
import random
import copy
import math
import time
class dmeyers3_ChessPlayer(ChessPlayer):

    def __init__(self, board, color):
        super().__init__(board, color)
        self.values_dict = {"queen":9, "princess":6, "rook": 5, "fool":3, "bishop": 3, "knight": 3, "pawn": 1, "king":0}
        self.num = 0

    def get_move(self, your_remaining_time, opp_remaining_time, prog_stuff):
        ####print  ("number 2 program")
        my_color = self.color
        ####print  (self.color)
        colors  = {}
        if my_color =="white":
            colors["max"] = 'white'
            colors["min"] = "black"
            
        else:
            colors["max"] = 'black'
            colors["min"] = "white"
       

        copy_board = copy.deepcopy(self.board)
        ####print  ("grade")
        ####print  (self.grade_min_grade_max(self.board,colors))

        max_moves = copy_board.get_all_available_legal_moves(colors["max"])
        min_moves = copy_board.get_all_available_legal_moves(colors["min"])

        ####print  ("beginning max")
        ####print  (max_moves)
        if len(max_moves) == 1:
            return max_moves[0]
        ####print  ("beginning min")
        ####print  (min_moves)

        total = len(max_moves) * len(min_moves)
        if len(min_moves) == 0:
            total = len(max_moves)
        print(self.board.is_king_in_check(colors["max"]))
        ####print  ("totals")
        ####print  (total)
        max_depth = math.trunc(150/total) * 2
        if max_depth < 2:
            max_depth = 2
        elif max_depth>4:
            max_depth =4
            if self.board.is_king_in_check(colors["max"]) == True:
                max_depth = 3
        ####print  ("DEPTHHHHH")
        ####print  (max_depth)

        start_time = time.time()

        move =  list(self.miniMax(colors,0,True,copy_board,max_depth, {},{0:1000000000}, {0:-100000000}, start_time).items())
        #print  (move)
        
        return move[0][0]

    def miniMax(self, color_dict, depth, maxTurn, board, targetDepth, move, currLow, currHigh,start_time ):
        self.num  = self.num + 1
        #print ("top")
        #print (currHigh)
        ##print  ("--- %s seconds ---" % (time.time() - start_time))
        ##print  (self.num)

        if (depth == targetDepth):
            if targetDepth<3 and self.piece_under_attack(board,color_dict,move):
                ####print  (self.num)
                targetDepth = targetDepth + 1
            else:
                game_board = board.get_all_available_legal_moves(color_dict["min"])
                return {(move[0], move[1]):self.evaluate(board, color_dict,move,currLow)}
        
        if (maxTurn):
            game_board = board.get_all_available_legal_moves(color_dict["max"])
            for i in range(len(game_board)):
                next_board = copy.deepcopy(board)
                next_board.make_move(game_board[i][0],game_board[i][1])
                

                


                new_dict = self.miniMax(color_dict, depth + 1,
                        False, next_board, targetDepth, game_board[i], currLow, currHigh,start_time)
                if type(new_dict) == type([]):
                    return new_dict[1]

                if new_dict != None:
                    if list(new_dict.values())[0]< list(currLow.values())[0]:
                        #print ("hereeeeeeeeeeeeeeeee low")
                        #print (new_dict)
                        #print (move)
                        currLow = {(game_board[i][0],game_board[i][1]): list(new_dict.values())[0]}

                if new_dict != None and list(currLow.values())[0] <= list(currHigh.values())[0]:
                    print ("break")
                    break
                

            return currLow

        
        else:
            
            game_board = board.get_all_available_legal_moves(color_dict["min"])
            if( board.is_king_in_checkmate(color_dict["min"]) and depth==1):
                ####print  ("gotcha")
                ####print  (move)
                ####print  (currLow)
                return ["gotcha", {move:0}]
            
            for i in range(len(game_board)):
                #print (currHigh)
                next_board = copy.deepcopy(board)
                next_board.make_move(game_board[i][0],game_board[i][1])

               
                new_dict = self.miniMax(color_dict, depth + 1,
                        True, next_board, targetDepth, game_board[i], currLow, currHigh,start_time)

                
                if new_dict != None:
                    if list(new_dict.values())[0]> list(currHigh.values())[0]:
                        
                        #print (new_dict)
                        currHigh = new_dict
                    
                
                if new_dict != None and list(currLow.values())[0]<= list(currHigh.values())[0]:
                    break

            return currHigh


    def evaluate(self, board,colors, move,low):
        beg_min_num = self.grade_min_grade_max(self.board, colors)[1] - self.grade_min_grade_max(self.board, colors)[0]
        

        now_min_num = self.grade_min_grade_max(board, colors)[1] - self.grade_min_grade_max(board, colors)[0]
        eval = ( now_min_num -beg_min_num )*5

        if self.board.is_king_in_checkmate(colors["max"]):
            eval = 10000000000000

        if self.board.is_king_in_checkmate(colors["min"]):
            eval = -1000000000
        
        
        # if eval<0:
        #     ####print  (move)
        #     pass
        # if eval>0:
        #     pass
        #     ####print  (move)
        #     ####print  (low)
        #     ####print  (beg_min_num)
        #     ####print  (now_min_num)
        #     ####print  (eval)
        #     ####print  (len(board.get_all_available_legal_moves(colors["min"])) + eval)

        return len(board.get_all_available_legal_moves(colors["min"])) + eval


    def grade_min_grade_max(self,board, colors):
        white = 0
        black = 0
        for val in board.values():
            
            if val.color == "white":
                
                white = white + self.values_dict[val.name]

            if val.color == "black":
                black = black + self.values_dict[val.name]

        if colors["max"] == "white":
            return(white,black)

        else:
            return(black,white)
    def piece_under_attack(self,board,colors,min_move):
        moves = board.get_all_available_legal_moves(colors["max"])

        for move in moves:
            if move[1] == min_move[1]:
                return True

        return False



