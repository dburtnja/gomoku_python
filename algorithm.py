import random
from board import EMPTY_CELL, Board
from pattern_controller import PatternController, SimplePattern
from config import *

# from gomoku import BOARD_SIZE

# BOARD_SIZE = 19
# FIRST_PLAYER = 1
# SECOND_PLAYER = 2
# REC_DEPT = 2


class GomokuAlgorithm:

    def __init__(self, board, player_number, board_size):
        if not isinstance(board, Board):
            raise AttributeError("board parameter should be instance of Board class")
        self._board = board
        self._player_number = player_number
        self._pattern_controller = PatternController(PATTERNS_FILE)
        self._simple_patern = SimplePattern("XXXXX", 99999999)
        if player_number == FIRST_PLAYER:
            self._human_number = SECOND_PLAYER
        else:
            self._human_number = FIRST_PLAYER

        self._board_size = board_size
        self._five_row = False

    def calculate_position(self):
        cell = EMPTY_CELL
        return_col = -1
        return_row = -1
        score = -9999999999

        # перебираємо потенційні ячєйки для ходів, і отримуємо оцінку поточного ходу, якщо оцінка поточного ходу більша
        # за збережений хід, тоді переписуємо збережений хід. Якщо доска пуста, тоді ставимо камінь в центр .
        coord_list = self.createMoveList()

        for element in coord_list:
            cell = self._board.get_cell_by_index(element[0], element[1])
            self._board.put_player_by_coords(element[0], element[1], self._player_number)
            current_score = self.minmaxAlphaBeta(REC_DEPT, self._human_number, -9999999999, 9999999999, element[0], element[1])
            print(str(element[0]+1), str(element[1]+1) + " -> " + str(current_score))
            self._board.clear_cell_by_coords(element[0], element[1])
            if current_score > score:
                score = current_score
                return_col = element[0]
                return_row = element[1]
        if return_col == -1 and return_row == - 1:
            return int(BOARD_SIZE / 2), int(BOARD_SIZE / 2)

        # print(return_col, return_row)

        return return_col, return_row

    def get_player_number(self):
        return self._player_number

    # основний метод minmaxAB, check Google =)
    def minmaxAlphaBeta(self, dept, player, alpha, beta, x, y):
        # if dept == 0 or self._simple_patern.check_board(self._board, self._player_number) != 0:
        # return self._pattern_controller.get_board_value(self._board, self._player_number)
        if self.check_win(x, y):
            if player == self._player_number:
                return 9999999999
            else:
                return -9999999999
        if dept == 0:
            return self.evaluation()

        coord_list = self.createMoveList()
        if player == self._player_number:
            for element in coord_list:
                self._board.put_player_by_coords(element[0], element[1], player)
                alpha = max(self.minmaxAlphaBeta(dept - 1, self._human_number, alpha, beta, element[0], element[1]), alpha)

                self._board.clear_cell_by_coords(element[0], element[1])
                if alpha >= beta:
                    break
            return alpha
        else:
            for element in coord_list:
                self._board.put_player_by_coords(element[0], element[1], self._human_number)
                beta = min(self.minmaxAlphaBeta(dept - 1, self._player_number, alpha, beta, element[0], element[1]), beta)
                self._board.clear_cell_by_coords(element[0], element[1])
                if alpha >= beta:
                    break
            return beta

    # метод який створює набір координат по яким можна зробити хід
    def createMoveList(self):
        list = []
        for column_index in range(BOARD_SIZE - 1):
            for row_index in range(BOARD_SIZE - 1):
                cell = self._board.get_cell_by_index(column_index, row_index)
                if cell == EMPTY_CELL and self.adjacentPlaced(column_index, row_index):
                    list.append((column_index, row_index))
        return list

    # метод який перевіряє пусту ячєйку, якщо в неї є не пустий сусід, тоді її можна використати для потенційного ходу
    def adjacentPlaced(self, column_index, row_index):
        cell = EMPTY_CELL
        value = False

        if (self._board.get_cell_by_index(column_index, row_index) != EMPTY_CELL):
            return False
        val = [-1, 0, 1, -1, 0, 1, 1, -1, -1]

        for i in range(0, 3):
            for j in range(0, 3):
                # if column_index + i >= 0 and row_index + j >= 0 and column_index + i < BOARD_SIZE and row_index + j < BOARD_SIZE:
                cell = self._board.get_cell_by_index(column_index + i-1, row_index + j-1)
                if cell != EMPTY_CELL:
                    value = True
        # for i in range(8):
        #     if column_index + val[i] >= 0 and row_index + val[i] >= 0 and column_index + val[
        #         i] <= BOARD_SIZE - 1 and row_index + val[i] <= BOARD_SIZE - 1:
        #         cell = self._board.get_cell_by_index(column_index + val[i], row_index + val[i + 1])
        #         if cell != EMPTY_CELL:
        #             value = True

        return value

    def evaluation(self):
        M = 5
        N = BOARD_SIZE
        sum = 0
        computerPattern = [0,0,0,0,0,0,0]
        playerPattern = [0,0,0,0,0,0,0]

        for i in range(0, N):
            for j in range (0, N):
                cell = self._board.get_cell_by_index(i, j)
                if cell != EMPTY_CELL:
                    needMax = cell == self._player_number

                    sameSymbol = 1
                    k = 1
                    while i - k >= 0 and self._board.get_cell_by_index(i - k, j) == cell:
                        sameSymbol+=1
                        k+=1

                    l = 1
                    #consider value at i - k later to see if it's blocked or not
                    while i + l <= N-1 and self._board.get_cell_by_index(i + l, j) == cell:
                        sameSymbol+=1
                        l+=1

                    if sameSymbol >= M:
                        if needMax:
                            computerPattern[M] += 1
                        else:
                            playerPattern[M] += 1
                    elif sameSymbol >= M-1 and (self._board.get_cell_by_index(i -k, j) == EMPTY_CELL or self._board.get_cell_by_index(i +l, j) == EMPTY_CELL):
                        if needMax:
                            computerPattern[M-1] += 1
                        else:
                            playerPattern[M-1] += 1
                    elif sameSymbol >= M-2 and (self._board.get_cell_by_index(i -k, j) == EMPTY_CELL or self._board.get_cell_by_index(i +l, j) == EMPTY_CELL):
                        if needMax:
                            computerPattern[M-2] += 1
                        else:
                            playerPattern[M-2] += 1
                    elif sameSymbol >= M-2 and (self._board.get_cell_by_index(i -k, j) == EMPTY_CELL and self._board.get_cell_by_index(i +l, j) == EMPTY_CELL):
                        if needMax:
                            computerPattern[M-3] += 1
                        else:
                            playerPattern[M-3] += 1
                    elif sameSymbol >= M - 3 and self._board.get_cell_by_index(i -k, j) == EMPTY_CELL and self._board.get_cell_by_index(i +l, j) == EMPTY_CELL:
                        if needMax:
                            computerPattern[M - 4] += 1
                        else:
                            playerPattern[M - 4] += 1
                    #rows
                    sameSymbol = 1
                    k = 1
                    while j - k >= 0 and self._board.get_cell_by_index(i, j - k) == cell:
                        sameSymbol+=1
                        k+=1
                    l = 1
                    while j + l <= N - 1 and self._board.get_cell_by_index(i, j + l) == cell:
                        sameSymbol+=1
                        l+=1
                    if sameSymbol >= M:
                        if needMax:
                            computerPattern[M] += 1
                        else:
                            playerPattern[M] += 1
                    elif sameSymbol >= M-1 and (self._board.get_cell_by_index(i, j - k) == EMPTY_CELL or self._board.get_cell_by_index(i, j + l) == EMPTY_CELL):
                        if needMax:
                            computerPattern[M-1] += 1
                        else:
                            playerPattern[M-1] += 1
                    elif sameSymbol >= M-2 and (self._board.get_cell_by_index(i, j - k) == EMPTY_CELL or self._board.get_cell_by_index(i, j + l) == EMPTY_CELL):
                        if needMax:
                            computerPattern[M-2] += 1
                        else:
                            playerPattern[M-2] += 1
                    elif sameSymbol >= M-2 and (self._board.get_cell_by_index(i, j - k) == EMPTY_CELL and self._board.get_cell_by_index(i, j + l) == EMPTY_CELL):
                        if needMax:
                            computerPattern[M-3] += 1
                        else:
                            playerPattern[M-3] += 1
                    elif sameSymbol >= M - 3 and self._board.get_cell_by_index(i, j - k) == EMPTY_CELL and self._board.get_cell_by_index(i, j + l) == EMPTY_CELL:
                        if needMax:
                            computerPattern[M - 4] += 1
                        else:
                            playerPattern[M - 4] += 1
                    #main diagonal
                    sameSymbol = 1
                    k = 1
                    while i - k >= 0 and j - k >= 0 and self._board.get_cell_by_index(i - k, j - k) == cell:
                        sameSymbol+=1
                        k+=1

                    l = 1
                    while i + l <= N - 1 and j + l <= N - 1 and self._board.get_cell_by_index(i + l, j + l) == cell:
                        sameSymbol+=1
                        l+=1
                    if sameSymbol >= M:
                        if needMax:
                            computerPattern[M] += 1
                        else:
                            playerPattern[M] += 1
                    elif sameSymbol >= M-1 and (self._board.get_cell_by_index(i - k, j - k) == EMPTY_CELL or self._board.get_cell_by_index(i + l, j + l) == EMPTY_CELL):
                        if needMax:
                            computerPattern[M-1] += 1
                        else:
                            playerPattern[M-1] += 1
                    elif sameSymbol >= M-2 and (self._board.get_cell_by_index(i - k, j - k) == EMPTY_CELL or self._board.get_cell_by_index(i + l, j + l) == EMPTY_CELL):
                        if needMax:
                            computerPattern[M-2] += 1
                        else:
                            playerPattern[M-2] += 1
                    elif sameSymbol >= M-2 and (self._board.get_cell_by_index(i - k, j - k) == EMPTY_CELL and self._board.get_cell_by_index(i + l, j + l) == EMPTY_CELL):
                        if needMax:
                            computerPattern[M-3] += 1
                        else:
                            playerPattern[M-3] += 1
                    elif sameSymbol >= M - 3 and self._board.get_cell_by_index(i - k, j - k) == EMPTY_CELL and self._board.get_cell_by_index(i + l, j + l) == EMPTY_CELL:
                        if needMax:
                            computerPattern[M - 4] += 1
                        else:
                            playerPattern[M - 4] += 1
                    #reverse diagonal
                    sameSymbol = 1
                    k = 1
                    while i - k >= 0 and j + k <= N - 1 and self._board.get_cell_by_index(i - k, j + k) == cell:
                        sameSymbol+=1
                        k+=1


                    l = 1
                    while i + l <= N - 1 and j - l >= 0 and self._board.get_cell_by_index(i + l, j - l) == cell:
                        sameSymbol+=1
                        l+=1
                    if sameSymbol >= M:
                        if needMax:
                            computerPattern[M] += 1
                        else:
                            playerPattern[M] += 1
                    elif sameSymbol >= M-1 and (self._board.get_cell_by_index(i - k, j + k) == EMPTY_CELL or self._board.get_cell_by_index(i + l, j - l) == EMPTY_CELL):
                        if needMax:
                            computerPattern[M-1] += 1
                        else:
                            playerPattern[M-1] += 1
                    elif sameSymbol >= M-2 and (self._board.get_cell_by_index(i - k, j + k) == EMPTY_CELL or self._board.get_cell_by_index(i + l, j - l) == EMPTY_CELL):
                        if needMax:
                            computerPattern[M-2] += 1
                        else:
                            playerPattern[M-2] += 1
                    elif sameSymbol >= M-2 and (self._board.get_cell_by_index(i - k, j + k) == EMPTY_CELL and self._board.get_cell_by_index(i + l, j - l) == EMPTY_CELL):
                        if needMax:
                            computerPattern[M-3] += 1
                        else:
                            playerPattern[M-3] += 1
                    elif sameSymbol >= M - 3 and self._board.get_cell_by_index(i - k, j + k) == EMPTY_CELL and self._board.get_cell_by_index(i + l, j - l) == EMPTY_CELL:
                        if needMax:
                            computerPattern[M - 4] += 1
                        else:
                            playerPattern[M - 4] += 1

        if computerPattern[M] > 0:
            return 99999999
        if playerPattern[M] > 0:
            return -99999999

        x = 1
        sum += computerPattern[1]
        sum -= playerPattern[1] * 5
        for i in range (2, M+1):
            x *= 100
            sum += computerPattern[i] * x
            sum -= playerPattern[i] * x * 10

        return sum

    def check_win(self, x, y):
        return self.rowOfFive(x, y) or self.columnOfFive(x, y) or self.mainDiagnolOfFive(x, y) or self.reverseDiagnolOfFive(x, y)

    def rowOfFive(self, x, y):
        temp = 1
        i = 1
        five = False

        while y - i >= 0 and self._board.get_cell_by_index(x,y - i) == self._board.get_cell_by_index(x,y):
            temp+=1
            i+=1
        i = 1
        if temp >= 5:
            five = True
        temp = 1
        while y + i <= BOARD_SIZE - 1 and self._board.get_cell_by_index(x, y + i) == self._board.get_cell_by_index(x,y):
            temp+=1
            i+=1

        if temp >= 5:
            five = True
        return five

    def columnOfFive(self, x, y):
        temp = 1
        i = 1
        five = False

        while x - i >= 0 and self._board.get_cell_by_index(x - i, y) == self._board.get_cell_by_index(x,y):
            temp+=1
            i+=1
        i = 1
        if temp >= 5:
            five = True
        temp = 1
        while x + i <= BOARD_SIZE - 1 and self._board.get_cell_by_index(x + i, y) == self._board.get_cell_by_index(x,y):
            temp+=1
            i+=1
        return five

    def mainDiagnolOfFive(self, x, y):
        temp = 1
        i = 1
        five = False

        while x - i >= 0 and y - i >= 0 and self._board.get_cell_by_index(x - i, y - i) == self._board.get_cell_by_index(x,y):
            temp+=1
            i+=1
        i = 1
        if temp >= 5:
            five = True
        temp = 1
        while x + i <= BOARD_SIZE - 1 and y + i <= BOARD_SIZE - 1 and self._board.get_cell_by_index(x + i, y + i) == self._board.get_cell_by_index(x,y):
            temp+=1
            i+=1
        return five

    def reverseDiagnolOfFive(self, x, y):
        temp = 1
        i = 1
        five = False

        while x - i >= 0 and y - i >= 0 and self._board.get_cell_by_index(x - i, y + i) == self._board.get_cell_by_index(x, y):
            temp += 1
            i += 1
        i = 1
        if temp >= 5:
            five = True
        temp = 1
        while x + i <= BOARD_SIZE - 1 and y + i <= BOARD_SIZE - 1 and self._board.get_cell_by_index(x + i,y - i) == self._board.get_cell_by_index(x, y):
            temp += 1
            i += 1
        return five