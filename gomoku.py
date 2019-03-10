import pygame
from config import *
from board import Board, FIRST_PLAYER, SECOND_PLAYER
from algorithm import GomokuAlgorithm
from pattern_controller import PatternController


BOARD_LINE_WIDTH = 3
BOARD_SIZE = 19

ROCK_RADIOUS = 20


class App:

    def __init__(self, width, height, player_colors=(BLACK_COLOR, WHITE_COLOR)):
        if len(player_colors) != 2:
            raise AttributeError("Player colors should be two.")
        self._debug_mod = True
        self._player_colors = player_colors
        self._font = None
        self._size = self._weight, self._height = width, height
        self._display = None
        self._background = None
        self._image_surf = None
        self._running = True
        board_window_pixel_size = Board.get_appropriate_window_size(2 * width / 3, BOARD_SIZE)
        self._board = Board(BOARD_SIZE, int(width / 24), board_window_pixel_size)
        self._computer_player = GomokuAlgorithm(self._board, FIRST_PLAYER, BOARD_SIZE)
        self._changes = True
        self._pattern_controller = PatternController("patterns.txt")

    def _get_size(self):
        return self._display.get_size()

    def __draw_lines(self, surf, coordinates):
        last_coord = coordinates[-1]
        first_coord = coordinates[0]

        for i, coordinate in enumerate(coordinates, 1):
            text = self._font.render(str(i), True, BLACK_COLOR)
            surf.blit(text, (first_coord - 30, coordinate))
            surf.blit(text, (coordinate, first_coord - 30))
            pygame.draw.line(surf, BLACK_COLOR,
                             (first_coord, coordinate),
                             (last_coord, coordinate),
                             BOARD_LINE_WIDTH)
            pygame.draw.line(surf, BLACK_COLOR,
                             (coordinate, first_coord),
                             (coordinate, last_coord),
                             BOARD_LINE_WIDTH)

    def __create_background_image(self):
        image_surf = pygame.image.load("wildtextures-wooden-chopping-board-texture.jpg")
        image_surf = pygame.transform.scale(image_surf, self._size)
        self.__draw_lines(image_surf, self._board.get_coordinates())
        return image_surf

    def _init(self):
        pygame.init()
        self._font = pygame.font.SysFont(None, 30)
        self._image_surf = self.__create_background_image()
        self._display = pygame.display.set_mode(self._size, pygame.HWSURFACE)
        pygame.display.set_caption("Gomoku")
        # pygame.draw.circle(image_surf, BLACK_COLOR, (411, 411), 20)
        self._place_cells(self._image_surf, self._board.get_active_coordinates())
        self._display.blit(self._image_surf, (0, 0))
        pygame.display.flip()
        pygame.event.clear()

        # pygame.draw.circle(image_surf, BLACK_COLOR, (411, 411), 20)
        # self._display.blit(image_surf, (0, 0))
        # pygame.display.update()

    def _place_cells(self, surf, cells):
        for cell in cells:
            self._place_cell(surf, cell)

    def _place_cell(self, surf, cell):
        column, row, (column_pos, row_pos, player) = cell
        pygame.draw.circle(surf, self._player_colors[player - 1], (column, row), ROCK_RADIOUS)

    @staticmethod
    def _clean():
        pygame.quit()

    def execute(self):
        self._init()

        while self._running:
            pygame.time.delay(100)
            self._check_events()
            self._loop()
            if self._changes:
                self._render()
        self._clean()

    def _check_events(self):

        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                self._running = False
            if self._computer_player.get_player_number() != self._board.get_current_player() and \
                    event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._put_on_board(event.pos)

    def _loop(self):
        if self._board.get_current_player() == self._computer_player.get_player_number():
            position = self._computer_player.calculate_position()
            self._put_on_board(position, True)

    def _render(self):
        self._display.blit(self._image_surf, (0, 0))
        pygame.display.update()
        self._changes = False

    def _put_on_board(self, position, position_as_index=False):
        self._changes = True
        res = self._board.put_rock(self._board.get_current_player(), position, ROCK_RADIOUS, position_as_index)
        if res:
            if self._debug_mod:
                self._show_visible_board()
            self._place_cell(self._image_surf, res)
            val = self._pattern_controller.get_board_value(self._board, 1, 2)
            print(val)

    def _show_visible_board(self):
        [*left_top_coords, right, bottom] = self._board.get_visible_board_coordinates()
        # pygame.draw.rect(self._image_surf, DARK_GRAY_COLOR,
        #                  (*left_top_coords, right - left_top_coords[0], bottom - left_top_coords[1]))
        visible_surface = pygame.Surface((right - left_top_coords[0], bottom - left_top_coords[1]))
        visible_surface.set_alpha(100)
        visible_surface.fill(DARK_GRAY_COLOR)
        self._image_surf.blit(visible_surface, left_top_coords)


if __name__ == '__main__':
    app = App(1200, 900)
    app.execute()
