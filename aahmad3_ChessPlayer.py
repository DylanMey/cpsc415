from os import path
from chess_player import ChessPlayer
import random
from copy import deepcopy
import numpy as np

class aahmad3_ChessPlayer(ChessPlayer):

    def __init__(self, board, color):
        super().__init__(board, color)

    def get_move(self, your_remaining_time, opp_remaining_time, prog_stuff):
        # a = random.choice(self.board.get_all_available_legal_moves(self.color))
        temp_boards = deepcopy(self.board)
        available_moves = temp_boards.get_all_available_legal_moves(self.color)
        un_killable_moves = []
        best_move = 0
        for move in available_moves:
            second_temp_board = deepcopy(temp_boards)
            second_temp_board.make_move(move[0], move[1])
            status = self.evaluate(second_temp_board)
            if status == "NO":
                continue
            else:
                unkill_moves = [status, move]
                un_killable_moves.append(unkill_moves)
        if len(un_killable_moves) > 0:
            best_move = self.which_is_the_best_move(un_killable_moves)
        if best_move == 0:
            best_move_alpha = []
            old_opp_score = self.get_total_score(temp_boards,"black")
            for move in available_moves:
                second_temp_board = deepcopy(temp_boards)
                second_temp_board.make_move(move[0], move[1])
                opp_score = self.get_total_score(second_temp_board,"black")
                some_move = self.evaluate2(second_temp_board, old_opp_score, opp_score)
                some_move_alpha = [some_move, move]
                best_move_alpha.append(some_move_alpha)

            best_move = self.which_is_the_best_move(False, best_move_alpha)
            print(best_move_alpha)
            print(best_move)
        return best_move

    def evaluate2(self, temp_board, old_opp_score, opp_score):
        score = self.get_total_score(temp_board, self.color)
        difference = old_opp_score - opp_score
        check = []
        moves_black = temp_board.get_all_available_legal_moves("black")
        for move in moves_black:
            second_temp_board = deepcopy(temp_board)
            second_temp_board.make_move(move[0], move[1])
            new_score = self.get_total_score(second_temp_board, "white")
            diff = score - new_score
            check_score = difference - diff
            check.append(check_score)

        best_outcome = check[0]
        worst_outcome = check[0]
        for i in range(len(check)):
            if check[i] > best_outcome:
                best_outcome = check[i]
            if check[i] < worst_outcome:
                worst_outcome = check[i]

        return best_outcome, worst_outcome

    def evaluate(self, temp_board):
        if self.color == "white":
            score = self.get_total_score(temp_board, "white") #temp score
            moves_black = temp_board.get_all_available_legal_moves("black")
            for move in moves_black:
                second_temp_board = deepcopy(temp_board)
                # print(moves_black[i][0], moves_black[i][1])
                second_temp_board.make_move(move[0], move[1])
                new_score = self.get_total_score(second_temp_board, "white")
                if new_score < score:
                    return "NO"
            if score:
                return len(moves_black)

    def which_is_the_best_move(self, un_killable_move, best_move_alpha=False):
        if isinstance(un_killable_move, list):
            lowest_length = 10000
            best_moves = []
            best_move = 0
            for move in un_killable_move:
                if move[0] < lowest_length:
                    lowest_length = move[0]

            for move in un_killable_move:
                if move[0] == lowest_length:
                    best_moves.append(move[1])
            if len(best_moves) > 1:
                best_move = random.choice(best_moves)
            else:
                best_move = best_moves[0]

            return best_move
        elif isinstance(best_move_alpha, list):
            best_move_list = []
            print(best_move_alpha)
            for i in range(len(best_move_alpha)):
                sum = best_move_alpha[i][0][0] + best_move_alpha[i][0][1]
                best_move_list.append([sum, best_move_alpha[i][1]])
            first = best_move_list[0][1]
            best_sum = best_move_list[0][0]
            best_move = first
            for i in range(len(best_move_list)):
                if best_move_list[i][0] > best_sum:
                    best_sum = best_move_list[i][0]
                    best_move = best_move_list[i][1]
            if best_move == first:
                print("It is first")
            return best_move



    def get_total_score(self, temp_board, color):
        rook = 50
        bishop = 35
        queen = 100
        king = 1000
        pawn = 10
        knight = 30
        fool = 60
        princess = 75

        total_score = 0
        list = [str(i[1]) for i in temp_board.items() if color in str(i[1])]
        
        for i in range(len(list)):
            if "rook" in list[i]:
                total_score = total_score + rook
            if "knight" in list[i]:
                total_score = total_score + knight
            if "bishop" in list[i]:
                total_score = total_score + bishop
            if "queen" in list[i]:
                total_score = total_score + queen
            if "king" in list[i]:
                total_score = total_score + king
            if "pawn" in list[i]:
                total_score = total_score + pawn
            if "fool" in list[i]:
                total_score = total_score + fool
            if "princess" in list[i]:
                total_score = total_score + princess

        return total_score
            

        
        
