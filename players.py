from board import Board
from abc import abstractmethod
from time import time
from config import *
from algorithm import GomokuAlgorithm

class Player:

    def __init__(self, name, number, helper:GomokuAlgorithm=None):
        self._occupations_number = 0
        self._player_number = number
        self._name = name
        self._helper = helper

    def make_move(self, board: Board, view):
        """
        This method calculate move and return coordinates and time spend on move calculation.
        :param board: Board object
        :param view: event type object
        :return: move_coordinates, calculation_time
        """
        start = time()
        return self._calculate_move(board, view), time() - start

    def get_number(self):
        return self._player_number

    def get_name(self):
        return self._name

    @abstractmethod
    def _calculate_move(self, board: Board, view):
        pass


class HumanPlayer(Player):

    def _calculate_move(self, board: Board, view):
        while view.running():
            for event in view.get_events():
                if right_btn_mouse_click_event(event):
                    return board.get_indexes_by_coordinates(event.pos)
                if mouse_motion_event(event):
                    hover_coords = board.get_indexes_by_coordinates(event.pos)
                    if None not in hover_coords:
                        coords = board.get_coordinates()
                        view.update_hint((coords[hover_coords[COLUMNS]], coords[hover_coords[ROWS]]), self.get_number())
        return None



class ComputerPlayer(Player):
    
            
    def _calculate_move(self, board: Board, view):
        return self._helper.calculate_position()
