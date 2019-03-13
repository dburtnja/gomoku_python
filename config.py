import pygame


GAME_NAME = "Gomoku"

DARK_GRAY_COLOR = (64, 64, 64)
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
HINT_ALPHA = 150


BOARD_LINE_WIDTH = 3
BOARD_SIZE = 19

REC_DEPT = 0

ROCK_RADIOUS = 20

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900

PATTERNS_FILE = "patterns.txt"
GAME_BOARD_TEXTURES_FILE = "wildtextures-wooden-chopping-board-texture.jpg"
START_TEXTURES_FILE = "start-game-nachat-igru-start-start-the-game.jpg"


EMPTY_CELL = -1
FIRST_PLAYER = 0
SECOND_PLAYER = 1

COLUMNS = 0
ROWS = 1
CELL = 2

TOP_LEFT_CORNER = 0
BOTTOM_RIGHT_CORNER = 1

VISIBLE_ARIA_DISTANCE = 2


def right_btn_mouse_click_event(event):
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1


def mouse_motion_event(event):
    return event.type == pygame.MOUSEMOTION
