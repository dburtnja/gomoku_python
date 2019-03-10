
EMPTY_CELL = 0
FIRST_PLAYER = 1
SECOND_PLAYER = 2

COLUMNS = 0
ROWS = 1
CELL = 2

TOP_LEFT_CORNER = 0
BOTTOM_RIGHT_CORNER = 1

VISIBLE_ARIA_DISTANCE = 2


def get_start_point(board_size):
    column_center = int(board_size / 2)
    row_center = int(board_size / 2)
    return column_center, row_center


class PlayBoard:

    def __init__(self, board_size):
        self._rows_coordinates = []
        self._columns_coordinates = []
        self._rows = [
            [EMPTY_CELL for _row in range(board_size)]
            for _column in range(board_size)
        ]

    def get_active_coordinates(self):
        result = []

        for x, row in enumerate(self._rows):
            for y, cell in enumerate(row):
                if cell != EMPTY_CELL:
                    result.append((x, y, cell))
        return result

    def put_player(self, column, row, player):
        if self._rows[row][column] == EMPTY_CELL:
            self._rows[row][column] = player
            return True
        return False

    def get_cell(self, column, row):
        return self._rows[row][column]


class Board:

    def __init__(self, board_size, window_strt_position, window_size, players=(FIRST_PLAYER, SECOND_PLAYER)):
        self._board_size = board_size
        self._players = players
        self._current_player = players[0]
        self._min = None
        self._max = None
        self._move_number = 0
        self._coordinates = self._calculate_coordinates(board_size, window_strt_position, window_size)
        self._play_board = PlayBoard(board_size)
        half_board_size = int(board_size / 2)
        self._column_visible_min = half_board_size - VISIBLE_ARIA_DISTANCE
        self._column_visible_max = half_board_size + VISIBLE_ARIA_DISTANCE
        self._row_visible_min = half_board_size - VISIBLE_ARIA_DISTANCE
        self._row_visible_max = half_board_size + VISIBLE_ARIA_DISTANCE
        # start_point = get_start_point(board_size)
        # self._play_board.put_player(start_point[COLUMNS], start_point[ROWS], player_starts)

    def get_current_player(self):
        return self._current_player

    def get_coordinates(self):
        return self._coordinates

    @staticmethod
    def _calculate_coordinates(board_size, window_start_position, window_size):
        index_bord_size = board_size - 1
        distance = int(window_size / index_bord_size)
        window_size_with_start = window_size + window_start_position
        return [coord for coord in range(window_start_position, window_size_with_start + 1, distance)]

    def get_active_coordinates(self):
        result = []

        for active in self._play_board.get_active_coordinates():
            column_coord = self._coordinates[active[COLUMNS]]
            row_coord = self._coordinates[active[ROWS]]
            result.append((column_coord, row_coord, active))
        return result

    @classmethod
    def get_appropriate_window_size(cls, max_window_size, columns):
        columns -= 1
        return int(round(max_window_size / columns) * columns)

    def _coordinates_is_not_on_board(self, coord, distance):
        if self._min is None and self._max is None:
            self._min = self._coordinates[0] - distance
            self._max = self._coordinates[-1] + distance
            print(self._max, self._min)
        if self._min <= coord[COLUMNS] <= self._max and self._min <= coord[ROWS] <= self._max:
            return False
        print("not on bord")
        return True

    def _change_player(self):
        for player in self._players:
            if self._current_player != player:
                self._current_player = player
                return

    def _get_index(self, rock_coordinates, distance):
        column = None
        row = None

        if self._coordinates_is_not_on_board(rock_coordinates, distance):
            return None, None
        for index, coordinate in enumerate(self._coordinates):
            min_coord = coordinate - distance
            max_coord = coordinate + distance
            if column is None and min_coord <= rock_coordinates[COLUMNS] <= max_coord:
                column = index
            if row is None and min_coord <= rock_coordinates[ROWS] <= max_coord:
                row = index
        return column, row

    def put_rock(self, player, rock_coordinates, distance, index_coordinates=False):
        if not index_coordinates:
            column, row = self._get_index(rock_coordinates, distance)
        else:
            column, row = rock_coordinates

        if column is not None and row is not None and self._play_board.put_player(column, row, player):
            self._change_player()
            self._change_visible_area(column, row)
            print(self.get_visible_board_coordinates())
            return self._coordinates[column], self._coordinates[row], (column, row, player)
        return False

    def get_cell_by_index(self, column_index, row_index):
        if column_index >= self._board_size or row_index >= self._board_size:
            return None
        return self._play_board.get_cell(column_index, row_index)

    def get_cell_by_index_on_visible_board(self, column_index, row_index):
        column_index += self._column_visible_min
        row_index += self._row_visible_min
        if column_index >= self._column_visible_max or row_index >= self._row_visible_max:
            return None
        return self._play_board.get_cell(column_index, row_index)

    def get_visible_board_size(self):
        """
        This method return visible bord size as tuple.
        :return: (columns_size, row_size)
        """
        return self._column_visible_max - self._column_visible_min, self._row_visible_max - self._row_visible_min

    def _change_visible_area(self, column_index, row_index):
        self._column_visible_min = self.__get_min(self._column_visible_min, column_index - VISIBLE_ARIA_DISTANCE, 0)
        self._column_visible_max = self.__get_max(self._column_visible_max, column_index + VISIBLE_ARIA_DISTANCE,
                                                  self._board_size - 1)
        self._row_visible_min = self.__get_min(self._row_visible_min, row_index - VISIBLE_ARIA_DISTANCE, 0)
        self._row_visible_max = self.__get_max(self._row_visible_max, row_index + VISIBLE_ARIA_DISTANCE,
                                               self._board_size - 1)
        print(column_index, row_index)
        print(self._column_visible_min, self._column_visible_max, self._row_visible_min, self._row_visible_max)

    @staticmethod
    def __get_min(current_min, available_min, min_value):
        if current_min > available_min:
            if available_min < min_value:
                return min_value
            return available_min
        return current_min

    @staticmethod
    def __get_max(current_max, available_max, max_value):
        if current_max < available_max:
            if available_max > max_value:
                return max_value
            return available_max
        return current_max

    def get_visible_board_coordinates(self):
        return self._coordinates[self._column_visible_min], self._coordinates[self._row_visible_min], \
               self._coordinates[self._column_visible_max], self._coordinates[self._row_visible_max]


if __name__ == '__main__':
    board = Board(19, 50, 720)
    # print(list(range(0, 19, 2)))
