from config import *
from board import Board, FIRST_PLAYER, SECOND_PLAYER
from pattern_controller import PatternController
from players import HumanPlayer, ComputerPlayer
from algorithm import GomokuAlgorithm
import pygame


class View:

    def __init__(self, width, height, name, player_colors=(BLACK_COLOR, WHITE_COLOR), sleep=100):
        if len(player_colors) != 2:
            raise AttributeError("Player colors should be two.")
        self._running = True
        self._size = self._width, self._height = width, height
        self._sleep = sleep
        self._player_colors = player_colors

        pygame.init()
        pygame.display.set_caption(name)
        self._font = pygame.font.SysFont(None, 30)

        self._display = pygame.display.set_mode(self._size, pygame.HWSURFACE)
        self._game_board_background_surf = None
        self._game_board_surf = None
        self._visible_board_surf_coord = None
        self._visible_board_surf = None

    @staticmethod
    def waiting_for_event():
        pygame.event.wait()

    def __del__(self):
        pygame.quit()

    def running(self):
        pygame.time.delay(self._sleep)
        return self._running

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            yield event

    def show_start_window(self, image_file):
        image_surf = self._create_image_surf(image_file, self._size)
        self._display.blit(image_surf, (0, 0))
        pygame.display.flip()
        pygame.event.clear()
        while self.running():
            for event in self.get_events():
                if right_btn_mouse_click_event(event):
                    return

    def show_play_window(self, image_file, board):
        self._game_board_background_surf = self._create_image_surf(image_file, self._size)
        self.__draw_lines(self._game_board_background_surf, board.get_coordinates())
        self._game_board_surf = pygame.Surface(self._size, pygame.SRCALPHA)
        self._place_cells(self._game_board_surf, board.get_active_coordinates())
        self._game_board_background_surf.convert()

        (*vis_board_cord, x_size, y_size) = board.get_visible_board()
        self._visible_board_surf = pygame.Surface((x_size, y_size))
        self._visible_board_surf.set_alpha(100)
        self._visible_board_surf.fill(DARK_GRAY_COLOR)

        self._visible_board_surf_coord = vis_board_cord
        self._display.blit(self._game_board_surf, (0, 0))
        self._display.blit(self._game_board_background_surf, (0, 0))
        pygame.display.flip()

    @staticmethod
    def _create_image_surf(image, size):
        image_surf = pygame.image.load(image)
        image_surf = pygame.transform.scale(image_surf, size)
        return image_surf

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

    def _place_cells(self, surf, cells):
        for cell in cells:
            self._place_cell(surf, cell)

    def _place_cell(self, surf, cell):
        column, row, (column_pos, row_pos, player) = cell
        pygame.draw.circle(surf, self._player_colors[player - 1], (column, row), ROCK_RADIOUS)

    def show_changes(self, board: Board, **kwargs):
        if "coordinate" in kwargs:
            self._place_cell(self._game_board_surf, kwargs.get("coordinate"))
        if kwargs.get("visible_board"):
            self._update_visible_board(board)
        self._update_surfaces()

    def update_hint(self, coordinates, player):
        hint_surf = pygame.Surface(self._size, pygame.SRCALPHA)
        column, row = coordinates
        pygame.draw.circle(hint_surf, (*self._player_colors[player - 1], HINT_ALPHA), (column, row), ROCK_RADIOUS)
        self._update_surfaces(((hint_surf, (0, 0)), ))

    def _update_visible_board(self, board):
        visible_board_coordinates = board.get_visible_board()
        self._visible_board_surf_coord = visible_board_coordinates
        self._visible_board_surf = pygame.Surface(visible_board_coordinates[2:])
        self._visible_board_surf.set_alpha(100)
        self._visible_board_surf.fill(DARK_GRAY_COLOR)

    def _update_surfaces(self, surfaces=(), size=None):
        if size is None:
            size = (0, 0, *self._size)
        surfaces = (
            (self._game_board_background_surf, (0, 0)),
            (self._game_board_surf, (0, 0)),
            (self._visible_board_surf, self._visible_board_surf_coord),
            *surfaces
        )
        for surface in surfaces:
            self._display.blit(*surface)
        pygame.display.update(pygame.Rect(size))


class App:

    def __init__(self):
        third_window_size = 2 * WINDOW_WIDTH / 3
        board_window_pixel_size = Board.get_appropriate_window_size(third_window_size, BOARD_SIZE)
        self._board = Board(BOARD_SIZE, int(WINDOW_WIDTH / 24), board_window_pixel_size)
        self._view = View(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_NAME, sleep=10)
        self._pattern_controller = PatternController(PATTERNS_FILE)
        self._players = None

    def _set_players(self):
        self._players = HumanPlayer("First", FIRST_PLAYER), ComputerPlayer("Second", SECOND_PLAYER, GomokuAlgorithm(self._board,SECOND_PLAYER, BOARD_SIZE))
        # self._players = HumanPlayer("First", FIRST_PLAYER), HumanPlayer("Second", SECOND_PLAYER)

    def _get_player(self, player_number):
        return self._players[player_number]

    def execute(self):
        self._view.show_start_window(START_TEXTURES_FILE)
        self._set_players()

        self._view.show_play_window(GAME_BOARD_TEXTURES_FILE, self._board)

        while self._view.running():
            self._make_moves()

    def _make_moves(self):
        player = self._get_player(self._board.get_current_player())
        coords, thinking_time = player.make_move(self._board, self._view)
        if coords:
            full_coords = self._board.put_rock(coords)
            if full_coords:
                self._view.show_changes(self._board, coordinate=full_coords, visible_board=True)
                print(player.get_name())
                print(f"Player {player.get_name()}: "
                      f"board_score={self._pattern_controller.get_board_value(self._board, player.get_number())},"
                      f"time={thinking_time}")



if __name__ == '__main__':
    app = App()
    app.execute()



# class App:
#
#     def __init__(self, width, height, player_colors=(BLACK_COLOR, WHITE_COLOR)):
#         if len(player_colors) != 2:
#             raise AttributeError("Player colors should be two.")
#         self._debug_mod = True
#         self._player_colors = player_colors
#         self._font = None
#         self._size = self._weight, self._height = width, height
#         self._display = None
#         self._background = None
#         self._image_surf = None
#         self._running = True
#         board_window_pixel_size = Board.get_appropriate_window_size(2 * width / 3, BOARD_SIZE)
#         self._board = Board(BOARD_SIZE, int(width / 24), board_window_pixel_size)
#         self._computer_player = GomokuAlgorithm(self._board, FIRST_PLAYER, BOARD_SIZE)
#         self._changes = True
#         self._pattern_controller = PatternController("patterns.txt")
#
#     def _get_size(self):
#         return self._display.get_size()
#
#     def __draw_lines(self, surf, coordinates):
#         last_coord = coordinates[-1]
#         first_coord = coordinates[0]
#
#         for i, coordinate in enumerate(coordinates, 1):
#             text = self._font.render(str(i), True, BLACK_COLOR)
#             surf.blit(text, (first_coord - 30, coordinate))
#             surf.blit(text, (coordinate, first_coord - 30))
#             pygame.draw.line(surf, BLACK_COLOR,
#                              (first_coord, coordinate),
#                              (last_coord, coordinate),
#                              BOARD_LINE_WIDTH)
#             pygame.draw.line(surf, BLACK_COLOR,
#                              (coordinate, first_coord),
#                              (coordinate, last_coord),
#                              BOARD_LINE_WIDTH)
#
#     def __create_background_image(self):
#         image_surf = pygame.image.load("wildtextures-wooden-chopping-board-texture.jpg")
#         image_surf = pygame.transform.scale(image_surf, self._size)
#         self.__draw_lines(image_surf, self._board.get_coordinates())
#         return image_surf
#
#     def _init(self):
#         pygame.init()
#         self._font = pygame.font.SysFont(None, 30)
#         self._image_surf = self.__create_background_image()
#         self._display = pygame.display.set_mode(self._size, pygame.HWSURFACE)
#         pygame.display.set_caption("Gomoku")
#         self._place_cells(self._image_surf, self._board.get_active_coordinates())
#         self._display.blit(self._image_surf, (0, 0))
#         pygame.display.flip()
#         pygame.event.clear()
#
#         # pygame.draw.circle(image_surf, BLACK_COLOR, (411, 411), 20)
#         # self._display.blit(image_surf, (0, 0))
#         # pygame.display.update()
#
#     def _place_cells(self, surf, cells):
#         for cell in cells:
#             self._place_cell(surf, cell)
#
#     def _place_cell(self, surf, cell):
#         column, row, (column_pos, row_pos, player) = cell
#         pygame.draw.circle(surf, self._player_colors[player - 1], (column, row), ROCK_RADIOUS)
#
#     @staticmethod
#     def _clean():
#         pygame.quit()
#
#     def execute(self):
#         self._init()
#
#         while self._running:
#             pygame.time.delay(100)
#             self._check_events()
#             self._loop()
#             if self._changes:
#                 self._render()
#         self._clean()
#
#     def _check_events(self):
#
#         for event in pygame.event.get():
#             # print(event)
#             if event.type == pygame.QUIT:
#                 self._running = False
#             if self._computer_player.get_player_number() != self._board.get_current_player() and \
#                     event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                 self._put_on_board(event.pos)
#
#     def _loop(self):
#         if self._board.get_current_player() == self._computer_player.get_player_number():
#             position = self._computer_player.calculate_position()
#             self._put_on_board(position, True)
#
#     def _render(self):
#         self._display.blit(self._image_surf, (0, 0))
#         pygame.display.update()
#         self._changes = False
#         val = self._pattern_controller.get_board_value(self._board, SECOND_PLAYER)
#
#     def _put_on_board(self, position, position_as_index=False):
#         self._changes = True
#         res = self._board.put_rock(self._board.get_current_player(), position, ROCK_RADIOUS, position_as_index)
#         if res:
#             if self._debug_mod:
#                 self._show_visible_board()
#             self._place_cell(self._image_surf, res)
#
#     def _show_visible_board(self):
#         [*left_top_coords, right, bottom] = self._board.get_visible_board_coordinates()
#         # pygame.draw.rect(self._image_surf, DARK_GRAY_COLOR,
#         #                  (*left_top_coords, right - left_top_coords[0], bottom - left_top_coords[1]))
#         visible_surface = pygame.Surface((right - left_top_coords[0], bottom - left_top_coords[1]))
#         visible_surface.set_alpha(100)
#         visible_surface.fill(DARK_GRAY_COLOR)
#         self._image_surf.blit(visible_surface, left_top_coords)
#

