from abc import abstractmethod
from board import Board, COLUMNS, ROWS, EMPTY_CELL, FIRST_PLAYER, SECOND_PLAYER

FILLED_CELL = 'X'
EMPTY_CELL_CHAR = '-'


CHECK_DIRECTIONS = [
    (-1, -1),
    (1, -1),
    (-1, 1),
    (1, 1),
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0)
]


class Pattern:
    """
    Base Pattern class. All patterns should be inherited from this class.
    """

    def __init__(self, pattern_description: str, score: int):
        self._pattern = self._parse_pattern(pattern_description)
        self._score = score
        self._size = len(self._pattern)
        self._directions = tuple(
            tuple([(number * column_mult, number * row_mult) for number in range(self._size)][::-1])
            for column_mult, row_mult in CHECK_DIRECTIONS
        )
        # print(list(self._directions))

    @classmethod
    @abstractmethod
    def can_parse(cls, pattern_string: str):
        pass

    @staticmethod
    def _check_available_chars_in_string(string, available_chars):
        for char in string:
            if char not in available_chars:
                return False
        return True

    def _board_size_is_suitable(self, column_size, row_size):
        if column_size > self._size or row_size > self._size:
            return False
        return True

    @abstractmethod
    def _parse_pattern(self, pattern_description: str):
        pass

    def check_board(self, board: Board, positive_player):
        """
        This method count all scores of current pattern on bord.
        :param board: Board object
        :param positive_player: player on witch score is adding
        :return: score sum
        """
        if not isinstance(board, Board):
            raise AttributeError(f"board parameter should be instance of Board class. Not: '{type(board)}'.")
        return self._check_board(board, positive_player)

    def __repr__(self):
        return f"{self._pattern} = {self._score}"

    @abstractmethod
    def _check_board(self, board, positive_player):
        pass


class SimplePattern(Pattern):
    """
    Simple pattern class. Example: -XXX-
    """

    def _check_board(self, board, positive_player):
        result = 0

        column_size, row_size = board.get_visible_board_size()
        for column in range(column_size):
            for row in range(row_size):
                for list_coordinates in self._directions:
                    temp_result, player = self._check_coordinates(column, row, list_coordinates, board)
                    if player == positive_player:
                        result += temp_result
                    else:
                        result -= temp_result
        return result

    def _check_coordinates(self, start_column, start_row, list_coordinates, board: Board):
        """
        This method compare coordinates with pattern, and return player and score for that player
        :param start_column: start column index
        :param start_row: start row index
        :param list_coordinates: list of coordinates to check (starts from zero, this method will add start coordinates)
        :param board: board object
        :return: score, player_number
        """
        player = None

        for i, (column_index, row_index) in enumerate(list_coordinates):
            cell = board.get_cell_by_index_on_visible_board(
                column_index + start_column,
                row_index + start_row
            )
            if cell is None or (cell == EMPTY_CELL and cell != self._pattern[i]):  # or not self._pattern[i]
                return 0, 0
            if cell == EMPTY_CELL:
                continue
            if player is None:
                player = cell
            if player != cell:
                return 0, 0
        return self._score, player

    @classmethod
    def can_parse(cls, pattern_string: str):
        return cls._check_available_chars_in_string(pattern_string, (EMPTY_CELL_CHAR, FILLED_CELL))

    def _parse_pattern(self, pattern_description):
        return tuple([True if char == FILLED_CELL else EMPTY_CELL for char in pattern_description][::-1])


class PatternFactory:
    """
    This class create Patterns based on they description.
    """

    def __init__(self, *available_patterns: type(Pattern)):
        if len(available_patterns) < 1:
            raise ValueError("Should be at least one pattern.")
        self._patterns = available_patterns

    def get_pattern(self, pattern_description):
        pattern_string, score = self._read_pattern(pattern_description)
        if score.isdigit():
            score = int(score)
        else:
            raise ValueError(f"Score value should be int type, not: '{score}'.")

        for pattern in self._patterns:
            if pattern.can_parse(pattern_string):
                return pattern(pattern_string, score)
        raise RuntimeError(f"Can find appropriate pattern class for such pattern: '{pattern_string}'.")

    @staticmethod
    def _read_pattern(pattern_description:str):
        """
        This method split pattern description string and check if it's valid.
        :param pattern_description: string: <pattenr>=<pattern_value> example: XXXXX=10000
        :return: pattern_string, score
        """
        if pattern_description.startswith("#"):
            raise ValueError("Most likely this string is a comment or you should remove '#' symbol.")
        if pattern_description == "":
            raise ValueError("Empty string can't be pattern.")
        pattern_list = pattern_description.split("=")
        if len(pattern_list) != 2:
            raise ValueError(f"Invalid input string: '{pattern_description}'.")
        return pattern_list


class PatternController:

    def __init__(self, patterns_path):
        pattern_factory = PatternFactory(SimplePattern)
        self._patterns = []
        with open(patterns_path, "r") as pattern_file:
            self._patterns = [pattern_factory.get_pattern(pattern_string.strip())
                              for pattern_string in pattern_file.readlines()
                              if pattern_string.strip() and not pattern_string.startswith("#")]

    def get_board_value(self, board, positive_player):
        """
        This method evaluates value on board.
        :param board:
        :param positive_player:
        :param negative_player:
        :return:
        """
        result = 0

        for pattern in self._patterns:
            result += pattern.check_board(board, positive_player)
        return result


if __name__ == '__main__':
    print("TEST PATTERN CONTROLLER")
    try:
        PatternController("patterns.txt")
    except Exception as e:
        print(e)
