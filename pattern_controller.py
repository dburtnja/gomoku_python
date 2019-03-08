from abc import abstractmethod

FILLED_CELL = 'X'
EMPTY_CELL = '-'


class Pattern:
    """
    Base Pattern class. All patterns should be inherited from this class.
    """

    def __init__(self, pattern_description: str, score: int):
        self._pattern = self._parse_pattern(pattern_description)
        self._score = score

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

    @abstractmethod
    def _parse_pattern(self, pattern_description:str):
        pass

    def __repr__(self):
        return f"{self._pattern} = {self._score}"


class SimplePattern(Pattern):
    """
    Simple pattern class. Example: -XXX-
    """

    @classmethod
    def can_parse(cls, pattern_string: str):
        return cls._check_available_chars_in_string(pattern_string, (EMPTY_CELL, FILLED_CELL))

    def _parse_pattern(self, pattern_description):
        return [True if char == FILLED_CELL else False for char in pattern_description]


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
        print(self._patterns)


if __name__ == '__main__':
    print("TEST PATTERN CONTROLLER")
    # try:
    PatternController("patterns.txt")
