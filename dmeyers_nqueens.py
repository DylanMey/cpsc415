import sys
import copy
import random
import time
import Dylans_chess_view

import multiprocessing


def main():
    

    if len(sys.argv)==1:
        print("There has to be atleast one argument")
        sys.exit(2)
    try:
        board_size = int(sys.argv[1])
    except:
        print("argument has to be a number")
    if len(sys.argv)>2:
        print(sys.argv)
        print("Too many arguments")
        sys.exit(2)
    full_board = []
    quit = multiprocessing.Event()
    foundit = multiprocessing.Event()
    
    for i in range(board_size):
        temp_row = []
        for x in range(board_size):
            temp_row.append(".")
            
        full_board.append(temp_row)
       

    
    # board = random_board(board)
    board, queens_list = random_board(full_board)
    solution_1 = print_current_try(queens_list)
    print(solution_1)
    # print(solution_1)
    Dylans_chess_view.game(len(board),solution_1, complete_move_list(board))
    
    start_time = time.time()
        
# multiprocessing.cpu_count()
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []
    print(multiprocessing.cpu_count())
    for i in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=loop, args=(board, return_dict,i,quit,foundit,full_board))
        jobs.append(p)
        p.start()

    
    foundit.wait()
    quit.set()

    # print("values2")
    # print(return_dict)
   

    board = return_dict.values()[0]
    queens_list = return_dict.values()[1]

    # print(queens_list)
    solution = print_current_try(queens_list)
    print("complete")
    print(complete_move_list(board))
    print("--- %s seconds ---" % (time.time() - start_time))

    Dylans_chess_view.game(len(board),solution, complete_move_list(board))
    
    
def loop(board,return_dict,num,quit,foundit,full_board):
    all_tries = []
    count = 0
    num = 1
    queens_list = []
    board,queens_list = random_board(full_board)
    print_current_try(queens_list)

    while not quit.is_set():
        curr_try = print_current_try(queens_list)
        all_tries.append(curr_try)
        if all_tries.count(curr_try)>2:
            board, queens_list = random_board(full_board)
            
            all_tries = []
        
        best = find_best_current_move(board,queens_list)

        count = count + 1
        
        
        # rand = random.choice(all_available_moves(board))
        # new_board = copy.deepcopy(make_move(board,rand))
        # while evaluation(board)<=evaluation(new_board):
        #     rand = random.choice(all_available_moves(board))
        #     new_board = copy.deepcopy(make_move(board,rand))
            
        # if len(moves)>0:
            
        #     best = random.choice(moves)
        # else:
        #     print("empty")
        #     random.choice(all_available_moves(board))
        

            
        
        
        
        # print("best")
        # print(best)
        # print("here")
        # print(board)
        # print(queens_list)
        # print(best)

        queens_list = copy.deepcopy(update_queens(best, queens_list))


        board = make_move(board,best)
        # print(board)
        # print("after")
        num = num + 1
        if board_solution(board,queens_list) == True:
            # print("Break")
            return_dict[num] = board
            return_dict["queen"] = queens_list
            # print(return_dict[num])
            foundit.set()
            
            break
    # print(f"end{num}")
    
    
def update_queens(move,queens_list):
    queens_list = copy.deepcopy(queens_list)
    for num,queen in enumerate(queens_list):
            moves_1 = move[0].split(",")
            if queens_list[num][0] == int(moves_1[0]) and queens_list[num][1] == int(moves_1[1]):
                moves_2 = move[1].split(",")
                queens_list[num] = (int(moves_2[0]), int(moves_2[1]))
    return queens_list
def board_solution(board,queen):

    for x,value in enumerate(queen):
            if check_queen(queen,(value[0],value[1]))>0:


                return False
    return True

def check_queen(queen, curr_queen):
    num = 0
    for x, value in enumerate(queen):
        # print("valuees")
        # print(value)
        if value[0] == curr_queen[0] and value[1] == curr_queen[1]:
            continue
        elif value[0] == curr_queen[0] or value[1] == curr_queen[1] or curr_queen[0] + curr_queen[1] == value[0] + value[1] or curr_queen[0] -value[0] == curr_queen[1]- value[1]:
            num = num + 1

        
    return num

def find_best_current_move(board,queens_list):
    min_eval = 1000
    min_move = 0
    count = 0
    for move in all_available_moves(board,queens_list):
        count = count + 1

        # print(move)
        temp_board = copy.deepcopy(board)
        
        # print("move")
        # print(move)
        temp_board = make_move(temp_board,move)
        new_queens_list = copy.deepcopy(update_queens(move, queens_list))
        # print(new_queens_list)
        # print(move)


        temp_eval = evaluation(new_queens_list)
        
        



        if temp_eval< min_eval:
            min_eval = temp_eval
            min_move = move
    # print("min")
    # print(min_eval)
    # print("checking")
    # print(min_move)
    return min_move
def find_better_moves(board,queens_list):
    min_eval = evaluation(queens_list)
    min_moves = []
    count = 0
    for move in all_available_moves(board,queens_list):
        
        count = count + 1

        # print(move)
        temp_board = copy.deepcopy(board)
        
        # print("move")
        # print(move)
        temp_board = make_move(temp_board,move)


        temp_eval = evaluation(queens_list)
        


        if temp_eval< min_eval:
            min_moves.append(move)
    return min_moves
    
    
def make_move(board, move):

    beg = move[0].split(",")
    end = move[1].split(",")
    temp_board = copy.deepcopy(board)
    temp_board[int(beg[0])][int(beg[1])]= "."
    temp_board[int(end[0])][int(end[1])]= "Q"
    return temp_board
def evaluation(queen):
    eval = 0
    for i, value in enumerate(queen):
            eval = eval +  check_queen(queen, (value[0],value[1]))
            
    # print(eval)
    return eval

def all_available_moves(board,queens_list):
    full_list_moves = []
    num = 0
    for i, value in enumerate(queens_list):
        



        temp_list = [(f'{value[0]},{value[1]}', f'{l},{value[1]}') for l in range(len(board)) if l != value[0]]

        full_list_moves = full_list_moves + temp_list

                
    
    return full_list_moves
                
def print_board(board):
    num = 0
    for row in board:

        print(f'{num}: {row}')
        num = num + 1
    print("     ", end = "")
    for i, value in enumerate(board):
        if i ==len(board) - 1:
            print("^")
        else:
            print("^", end ="    ")
    print("     ", end = "")
    for i, value in enumerate(board):
        print(i, end ="    ")



def print_current_try(queens_list):
    temp_dict = {}

    
    print("[", end = " ")
   
    # print(queens_list)

    for n, value in enumerate(queens_list):
            print(value[0], end= " ")
            temp_dict[value[1]] = value[0]
          
    print("]")

    # print(temp_dict)
    return temp_dict
def random_board(board):
    ran_list = []
    new_board = []
    queens_list = []
    new_board = copy.deepcopy(board)
    for i, value in enumerate(board):
        ran_list.append(random.randint(0,len(board)-1))

    for i, value in enumerate(ran_list):
        queens_list.append((value,i))

        new_board[value][i] = "Q"
    return new_board, queens_list
def complete_move_list(board):
    final_list = []
    for i, value in enumerate(board):
        for x, value in enumerate(board[i]):
            if board[i][x] == "Q":
                final_list = final_list +  queen_moves(board, (i,x))
    return final_list
 
def queen_moves(board, curr_queen):
    temp_list = []
    for i, value in enumerate(board):
        for x, value in enumerate(board[i]):
            
            if i == curr_queen[0] and x == curr_queen[1]:
                continue
            elif board[i][x] == "Q" and (i == curr_queen[0] or x == curr_queen[1] or curr_queen[0] + curr_queen[1] == x + i or curr_queen[0] -i == curr_queen[1]- x):
                temp_list.append((True,f'{curr_queen[0]},{curr_queen[1]}', f'{i},{x}') )
            elif i == curr_queen[0] or x == curr_queen[1] or curr_queen[0] + curr_queen[1] == x + i or curr_queen[0] -i == curr_queen[1]- x:
                temp_list.append((False,f'{curr_queen[0]},{curr_queen[1]}', f'{i},{x}') )


    return temp_list


    




if __name__ == "__main__":
    main()

