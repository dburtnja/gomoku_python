import random
from board import EMPTY_CELL, Board
# from gomoku import BOARD_SIZE

BOARD_SIZE = 19
FIRST_PLAYER = 1
SECOND_PLAYER = 2
REC_DEPT = 2

class GomokuAlgorithm:

    def __init__(self, board, player_number, board_size):
        if not isinstance(board, Board):
            raise AttributeError("board parameter should be instance of Board class")
        self._board = board
        self._player_number = player_number

        if player_number == FIRST_PLAYER:
            self._human_number = SECOND_PLAYER
        else:
            self._human_number = FIRST_PLAYER

        self._board_size = board_size

    def calculate_position(self):
        cell = EMPTY_CELL
        return_col = -1
        return_row = -1
        score = -9999999

        #перебираємо потенційні ячєйки для ходів, і отримуємо оцінку поточного ходу, якщо оцінка поточного ходу більша
        # за збережений хід, тоді переписуємо збережений хід. Якщо доска пуста, тоді ставимо камінь в центр.
        for column_index in range(BOARD_SIZE - 1):
            for row_index in range (BOARD_SIZE - 1):
                cell = self._board.get_cell_by_index(column_index, row_index)
                if cell == EMPTY_CELL and self.adjacentPlaced(column_index,row_index):
                    self._board.put_player_by_coords(column_index, row_index, self._player_number)
                    current_score = self.minmaxAlphaBeta(REC_DEPT, False, -9999999, 9999999)
                    # print(return_col, return_row + " -> " + current_score)
                    self._board.clear_cell_by_coords(column_index, row_index)
                    if current_score > score:
                        score = current_score
                        return_col = column_index
                        return_row = row_index
        if return_col == -1 and return_row == - 1:
            return int(BOARD_SIZE /2),int(BOARD_SIZE/2)

        print(return_col, return_row)

        return return_col,return_row
    def get_player_number(self):
        return self._player_number

    # основний метод minmaxAB, check Google =)
    def minmaxAlphaBeta(self, dept, isMax, alpha, beta):
        if dept == 0:
            return random.randint(-50, 50)
        coord_list = self.createMoveList()
        if isMax:
            for element in coord_list:
                self._board.put_player_by_coords(element[0], element[1], self._player_number)
                alpha = max(self.minmaxAlphaBeta(dept - 1, False, alpha, beta), alpha)

                self._board.clear_cell_by_coords(element[0], element[1])
                if alpha >= beta:
                    break
            return alpha
        else:
            for element in coord_list:
                self._board.put_player_by_coords(element[0], element[1], self._human_number)
                beta = min(self.minmaxAlphaBeta(dept - 1, True, alpha, beta), beta)
                self._board.clear_cell_by_coords(element[0], element[1])
                if alpha >= beta:
                    break
            return beta

    #метод який створює набір координат по яким можна зробити хід
    def createMoveList(self):
        list = []
        for column_index in range(BOARD_SIZE - 1):
            for row_index in range (BOARD_SIZE - 1):
                cell = self._board.get_cell_by_index(column_index, row_index)
                if cell == EMPTY_CELL and self.adjacentPlaced(column_index, row_index):
                    list.append((column_index,row_index))
        return list

    #метод який перевіряє пусту ячєйку, якщо в неї є не пустий сусід, тоді її можна використати для потенційного ходу
    def adjacentPlaced(self,column_index, row_index):
        cell = EMPTY_CELL
        value = False

        if (self._board.get_cell_by_index(column_index, row_index) != EMPTY_CELL):
            return False
        val = [-1, 0, 1, -1, 0, 1, 1,-1,-1]

        for i in range(8):
            if column_index + val[i] >=0 and  row_index + val[i] >=0 and column_index + val[i] <= BOARD_SIZE-1 and  row_index + val[i] <= BOARD_SIZE-1:
                cell = self._board.get_cell_by_index(column_index + val[i], row_index + val[i+1])
                if cell != EMPTY_CELL:
                    value = True

        return value
