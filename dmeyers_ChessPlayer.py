from chess_player import ChessPlayer
import random
import copy
import math
import time

class dmeyers_ChessPlayer(ChessPlayer):
    
    def __init__(self, board, color):
        super().__init__(board, color)
        self.values_dict = {"queen":9, "princess":6, "rook": 5, "fool":3, "bishop": 3, "knight": 3, "pawn": 1, "king":0}
        self.num = 0
        self.move = 0


    def get_move(self, your_remaining_time, opp_remaining_time, prog_stuff):
        self.move = self.move + 1
        self.num  = self.num + 1
        ##print("number 1 program")
        my_color = self.color
        ##print(self.color)
        colors  = {}
        if my_color =="white":
            colors["max"] = 'white'
            colors["min"] = "black"
            
        else:
            colors["max"] = 'black'
            colors["min"] = "white"




        copy_board = copy.deepcopy(self.board)
        ##print("HASHHHHH")
        ##print(hash(str(self.board)))
        ##print("grade")
        ##print(self.grade_min_grade_max(self.board,colors))

        max_moves = copy_board.get_all_available_legal_moves(colors["max"])
        min_moves = copy_board.get_all_available_legal_moves(colors["min"])

        ##print("beginning max")
        ##print(max_moves)
        if len(max_moves) == 1:
            return max_moves[0]
        ##print("beginning min")
        ##print(min_moves)

        total = len(max_moves) * len(min_moves)
        if len(min_moves) == 0:
            total = len(max_moves)

        ##print("totals")
        ##print(total)
        max_depth = math.trunc(100/total) * 2
        if max_depth < 2:
            max_depth = 2
        elif max_depth>4:
            max_depth = 4
        ##print("DEPTHHHHH")
        ##print(max_depth)

        start_time = time.time()

        move =  list(self.miniMax(colors,0,True,copy_board,max_depth, {},{0:1000000000}, {0:-100000000},True, start_time).items())
        ##print(move[0][0])
        print(move[0][0])
        return move[0][0]

    def miniMax(self, color_dict, depth, maxTurn, board, targetDepth, move, currLow, currHigh,null, start_time ):
        self.num  = self.num + 1
        print("First")
        print(self.num)
        print(print("--- %s seconds ---" % (time.time() - start_time)))
        
        if (depth == targetDepth):
            if targetDepth<3 and self.piece_under_attack(board,color_dict,move):
                #print(self.num)
                targetDepth = targetDepth + 1
            else:
                game_board = board.get_all_available_legal_moves(color_dict["min"])
                # if len(game_board) == 0:
                    ##print("depth")
                    ##print(depth)
                    ##print("herrrrrrrrrrrrrrrrrrrrrrrrre")
                return {(move[0], move[1]):self.evaluate(board, color_dict,move,currLow)}
        
        if (maxTurn):
            min_num = {0:1000000000}
            print("before")
            print("--- %s seconds ---" % (time.time() - start_time))
            game_board = self.reorder_board(board,color_dict["max"])
            
            print("second")
            print("--- %s seconds ---" % (time.time() - start_time))

            # game_board = board.get_all_available_legal_moves(color_dict["max"])
            for i in range(len(game_board)):
                next_board = copy.deepcopy(board)
                next_board.make_move(game_board[i][0],game_board[i][1])
                
                
# and self.zigzuang() == False 
                


                new_dict = self.miniMax(color_dict, depth + 1,
                        False, next_board, targetDepth, game_board[i], min_num, currHigh, True, start_time)
                
                if type(new_dict) == type([]) and new_dict[0] == "gotcha":
                    return new_dict[1]
                if type(new_dict) == type([]) and new_dict[0] == "null":
                    return new_dict[1]

                if new_dict != None and list(new_dict.values())[0]< list(min_num.values())[0]:
                    print(min_num)
                    min_num = {game_board[i]:list(new_dict.values())[0]}
                    print(min_num)



                if null and board.is_king_in_check(color_dict["max"]) == False and depth >1:
                    null_dict = self.miniMax(color_dict, depth+1, True, board, depth+2, move, currLow, currHigh,False,start_time )
                    #print(null_dict)
                    if list(currHigh.values())[0] >= list(null_dict.values())[0]:
                        print("here2")
                        return ["null",currHigh]
                print("third")
                print("--- %s seconds ---" % (time.time() - start_time))
                if new_dict != None and list(new_dict.values())[0]<list(currHigh.values())[0]:
                    return currHigh
            
            return min_num
        
        else:
            temp_dict = {}
            
            if( board.is_king_in_checkmate(color_dict["min"]) and depth==1):
                ##print("gotcha")
                ##print(move)
                ##print(currLow)
                return ["gotcha", {move:0}]
            game_board = self.reorder_board(board,color_dict["min"])
            # game_board = board.get_all_available_legal_moves(color_dict["max"])
            high_num = {0:-1000000000}
            for i in range(len(game_board)):
                next_board = copy.deepcopy(board)
                next_board.make_move(game_board[i][0],game_board[i][1])
                
                new_dict = self.miniMax(color_dict, depth + 1,
                        True, next_board, targetDepth, game_board[i], currLow, high_num,True,start_time)
                if type(new_dict) == type([]) and new_dict[0] == "null":
                    return new_dict[1]
                
                if new_dict != None and list(new_dict.values())[0]>list(high_num.values())[0]:
                    high_num = new_dict

                if null and board.is_king_in_check(color_dict["min"]) == False and depth >0 and list(currLow.values())[0] != 1000000000:
                    
                    null_dict = self.miniMax(color_dict, depth+1, False, board, depth+2, move, currLow, currHigh,False, start_time )
                    # #print(currLow)
                    # #print(temp_dict)
                    # #print(null_dict)
                    if null_dict != None and currLow != None and list(currLow.values())[0] <= list(null_dict.values())[0]:
                        print("here")
                        return["null",currLow]
                if new_dict != None and list(new_dict.values())[0]> list(currLow.values())[0]:
                    return currLow
                
            # ##print("min")
            # ##print(temp_dict)
            if len(temp_dict)>0:
                return high_num
            else:
                return None

    def evaluate(self, board,colors, move,low):
        beg_min_num = self.grade_min_grade_max(self.board, colors)[1] - self.grade_min_grade_max(self.board, colors)[0]
        

        now_min_num = self.grade_min_grade_max(board, colors)[1] - self.grade_min_grade_max(board, colors)[0]
        eval = ( now_min_num -beg_min_num )*5

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
    def reorder_board(self,board,color):
        ordered_dict = {}
        for move in board.get_all_available_legal_moves(color):
            if move[1] in board:
                new_val = self.values_dict[board[move[0]].name] - self.values_dict[board[move[1]].name]
                ordered_dict[move] = new_val
            else:
                ordered_dict[move] = 0
        return list({k: v for k, v in sorted(ordered_dict.items(), key=lambda item: item[1],reverse=True)}.keys())
    


        





        
        
        

        
        

                



