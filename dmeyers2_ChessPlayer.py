from chess_player import ChessPlayer
import random
import copy
import math
import time
class dmeyers2_ChessPlayer(ChessPlayer):

    def __init__(self, board, color):
        super().__init__(board, color)
        self.values_dict = {"queen":9, "princess":6, "rook": 5, "fool":3, "bishop": 3, "knight": 3, "pawn": 1, "king":0}
        self.num = 0

    def get_move(self, your_remaining_time, opp_remaining_time, prog_stuff):
        #print("number 2 program")
        my_color = self.color
        #print(self.color)
        colors  = {}
        if my_color =="white":
            colors["max"] = 'white'
            colors["min"] = "black"
            
        else:
            colors["max"] = 'black'
            colors["min"] = "white"
       

        copy_board = copy.deepcopy(self.board)
        #print("grade")
        #print(self.grade_min_grade_max(self.board,colors))

        max_moves = copy_board.get_all_available_legal_moves(colors["max"])
        min_moves = copy_board.get_all_available_legal_moves(colors["min"])

        #print("beginning max")
        #print(max_moves)
        if len(max_moves) == 1:
            return max_moves[0]
        #print("beginning min")
        #print(min_moves)

        total = len(max_moves) * len(min_moves)
        if len(min_moves) == 0:
            total = len(max_moves)

        #print("totals")
        #print(total)
        max_depth = math.trunc(100/total) * 2
        if max_depth < 2:
            max_depth = 2
        elif max_depth>4:
            max_depth =3
        #print("DEPTHHHHH")
        #print(max_depth)

        start_time = time.time()

        move =  list(self.miniMax(colors,0,True,copy_board,max_depth, {},1000000000, -100000000, start_time).items())
        #print(move[0][0])
        
        return move[0][0]

    def miniMax(self, color_dict, depth, maxTurn, board, targetDepth, move, currLow, currHigh,start_time ):
        # self.num  = self.num + 1
        # print(print("--- %s seconds ---" % (time.time() - start_time)))
        # print(self.num)

        if (depth == targetDepth):

            game_board = board.get_all_available_legal_moves(color_dict["min"])

            return {(move[0], move[1]):self.evaluate(board, color_dict,move,currLow)}
        
        if (maxTurn):
            temp_dict = {}
            game_board = board.get_all_available_legal_moves(color_dict["max"])
            
            for i in range(len(game_board)):
                next_board = copy.deepcopy(board)
                next_board.make_move(game_board[i][0],game_board[i][1])
                if len(temp_dict)>0:
                    min_num = temp_dict[min(temp_dict,  key=temp_dict.get)]
                else:
                    min_num = 1000000000


                new_dict = self.miniMax(color_dict, depth + 1,
                        False, next_board, targetDepth, game_board[i], min_num, currHigh,start_time)
                if type(new_dict) == type([]):
                    return new_dict[1]
                if new_dict != None:
                    temp_dict[game_board[i]] = list(new_dict.values())[0]
                if new_dict != None and list(new_dict.values())[0]<= currHigh:
                    print("BREAKKKKKKKKKKKKKKKKKKKK")
                    break
                
            
            if len(temp_dict)>0:
                # if depth == 0:
                    #print(temp_dict)
                return {min(temp_dict,  key=temp_dict.get):temp_dict[min(temp_dict,  key=temp_dict.get)]}
            else:
                return None
        
        else:
            temp_dict = {}
            
            game_board = board.get_all_available_legal_moves(color_dict["min"])
            if( board.is_king_in_checkmate(color_dict["min"]) and depth==1):
                #print("gotcha")
                #print(move)
                #print(currLow)
                return ["gotcha", {move:0}]
            
            for i in range(len(game_board)):
                next_board = copy.deepcopy(board)
                next_board.make_move(game_board[i][0],game_board[i][1])
                if len(temp_dict)>0:
                    high_num = temp_dict[max(temp_dict,  key=temp_dict.get)]
                else:
                    high_num = -1000000000
                new_dict = self.miniMax(color_dict, depth + 1,
                        True, next_board, targetDepth, game_board[i], currLow, high_num,start_time)
                if new_dict != None:
                    temp_dict.update(new_dict)
                if new_dict != None and list(new_dict.values())[0]>= currLow:
                    print("BREAKKKKKKKKKKKKKKK")
                    break
                
            # #print("min")
            # #print(temp_dict)
            if len(temp_dict)>0:
                return {max(temp_dict,  key=temp_dict.get):temp_dict[max(temp_dict,  key=temp_dict.get)]}
            else:
                return None

    def evaluate(self, board,colors, move,low):
        beg_min_num = self.grade_min_grade_max(self.board, colors)[1] - self.grade_min_grade_max(self.board, colors)[0]
        

        now_min_num = self.grade_min_grade_max(board, colors)[1] - self.grade_min_grade_max(board, colors)[0]
        eval = ( now_min_num -beg_min_num )*5
        
        
        # if eval<0:
        #     #print(move)
        #     pass
        # if eval>0:
        #     pass
        #     #print(move)
        #     #print(low)
        #     #print(beg_min_num)
        #     #print(now_min_num)
        #     #print(eval)
        #     #print(len(board.get_all_available_legal_moves(colors["min"])) + eval)

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



