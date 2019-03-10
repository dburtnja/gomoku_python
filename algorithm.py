import random
from board import EMPTY_CELL, Board
# from gomoku import BOARD_SIZE

BOARD_SIZE = 19
REC_DEPT = 0

class GomokuAlgorithm:

    def __init__(self, board, player_number, board_size):
        if not isinstance(board, Board):
            raise AttributeError("board parameter should be instance of Board class")
        self._board = board
        self._player_number = player_number
        self._board_size = board_size

    def calculate_position(self):
        while True:
            row_index = random.randint(0, self._board_size)
            column_index = random.randint(0, self._board_size)
            cell_val = self._board.get_cell_by_index(column_index, row_index)
            if cell_val == EMPTY_CELL:
                return column_index, row_index

        cell = EMPTY_CELL
        return_col = -1
        return_row = -1
        score = float('-inf')
        self.evaluation(5, 5)
        #перебираємо потенційні ячєйки для ходів, і отримуємо оцінку поточного ходу, якщо оцінка поточного ходу більша
        # за збережений хід, тоді переписуємо збережений хід. Якщо доска пуста, тоді ставимо камінь в центр.
        for column_index in range(BOARD_SIZE - 1):
            for row_index in range (BOARD_SIZE - 1):
                cell = self._board.get_cell_by_index(column_index, row_index)
                if cell == EMPTY_CELL and self.adjacentPlaced(column_index,row_index):
                    current_score = self.minmaxAlphaBeta(REC_DEPT, self._player_number, float('-inf'), float('inf'),column_index, row_index)
                    if current_score > score:
                        return_col = column_index
                        return_row = row_index
        if return_col == -1 and return_row == - 1:
            return int(BOARD_SIZE /2),int(BOARD_SIZE/2)
        return return_col,return_row
    def get_player_number(self):
        return self._player_number

    # основний метод minmaxAB, check Google =)
    def minmaxAlphaBeta(self, dept, player, alpha, beta, column_index,row_index):
        coord_list = []
        if dept == 0:
            # self.evaluation(column_index,row_index)
            return 0
        coord_list = self.createMoveList()
        self.minmaxAlphaBeta(dept - 1, player, alpha, beta, column_index, row_index)
        return 0

    #метод для оцінки ходу по патернам
    def evaluation(self, column_index, row_index ):
        toeval = [0,0,0,0,0]

        for i in range(5):
            cell = (self._board.get_cell_by_index(column_index + i, row_index))
            if (cell):
                toeval[i] = cell
                self.getCountForRow(toeval)
        for i in range(5):
            cell = (self._board.get_cell_by_index(column_index - i, row_index))
            if (cell):
                toeval[i] = cell
                self.getCountForRow(toeval)
        for i in range(5):
            cell = (self._board.get_cell_by_index(column_index + i, row_index + i))
            if (cell):
                toeval[i] = cell
                self.getCountForRow(toeval)
        for i in range(5):
            cell = (self._board.get_cell_by_index(column_index + i, row_index - i))
            if (cell):
                toeval[i] = cell
                self.getCountForRow(toeval)
        for i in range(5):
            cell = (self._board.get_cell_by_index(column_index - i, row_index - i))
            if (cell):
                toeval[i] = cell
                self.getCountForRow(toeval)
        for i in range(5):
            cell = (self._board.get_cell_by_index(column_index - i, row_index + i))
            if (cell):
                toeval[i] = cell
                self.getCountForRow(toeval)
        for i in range(5):
            cell = (self._board.get_cell_by_index(column_index, row_index + i))
            if (cell):
                toeval[i] = cell
                self.getCountForRow(toeval)
        for i in range(5):
            cell = (self._board.get_cell_by_index(column_index, row_index - i))
            if (cell):
                toeval[i] = cell
                self.getCountForRow(toeval)
        return 0

    def getCountForRow(self, row):
        value = 0
        sameSymbol = 0
        symbol = 0

        for i in range(5):
            if symbol == 0:
                if row[i] != 0 and symbol == 0:
                    symbol = row[i]
            if symbol == row[i]:
                sameSymbol = sameSymbol + 1
        print (sameSymbol)
        return value
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
        val = [-1, 0, 1, -1, 0, 1,1,-1,-1]

        for i in range(8):
            if column_index + val[i] >=0 and  row_index + val[i] >=0 and column_index + val[i] <= BOARD_SIZE-1 and  row_index + val[i] <= BOARD_SIZE-1:
                cell = self._board.get_cell_by_index(column_index + val[i], row_index + val[i+1])
                if cell != EMPTY_CELL:
                    value = True

        return value
