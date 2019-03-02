import random
from board import EMPTY_CELL, Board


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

    def get_player_number(self):
        return self._player_number
