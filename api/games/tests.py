import unittest

from django.test import TestCase
from games.services.boards import (
    generate_board,
    generate_map,
    calculate_board_cell_value,
    generate_adjacent_cells,
)
from games.utils import encode, decode


class TestGame:
    """
    # game_map visualization:
    T  F  F
    T  F  F
    F  F  F

    # game_board visualizaton:
    N  N  N
    -1 2  N
    N  N  0
    """

    def __init__(self):
        self.__game_map = {
            0: {
                0: {"is_bomb": True, "is_revealed": False},
                1: {"is_bomb": False, "is_revealed": False},
                2: {"is_bomb": False, "is_revealed": False},
            },
            1: {
                0: {"is_bomb": True, "is_revealed": True},
                1: {"is_bomb": False, "is_revealed": True},
                2: {"is_bomb": False, "is_revealed": False},
            },
            2: {
                0: {"is_bomb": False, "is_revealed": False},
                1: {"is_bomb": False, "is_revealed": False},
                2: {"is_bomb": False, "is_revealed": True},
            },
        }
        self.__game_board = [None, None, None, -1, 2, None, None, None, 0]

    def get_game_map(self):
        return self.__game_map

    def get_game_board(self):
        return self.__game_board


class TestBoardMethods(unittest.TestCase):
    def setUp(self):
        self.game = TestGame()

    def test_calculate_cell_value_in_board(self):
        game_map = self.game.get_game_map()
        # if it is not revealed: None
        self.assertEqual(calculate_board_cell_value(0, 0, game_map), None)
        self.assertEqual(calculate_board_cell_value(0, 1, game_map), None)
        # if it is revealed and a bomb: -1
        self.assertEqual(calculate_board_cell_value(1, 0, game_map), -1)
        # if it is is revealed and not a bomb: check adjacent cells
        self.assertEqual(calculate_board_cell_value(1, 1, game_map), 2)
        self.assertEqual(calculate_board_cell_value(2, 2, game_map), 0)

    def test_generate_map_size(self):
        board_size = 3
        game_map = generate_map(board_size)
        self.assertEqual(len(game_map.keys()), board_size)
        self.assertEqual(len(game_map[0].keys()), board_size)

    def test_generate_map_initial_values(self):
        board_size = 3
        game_map = generate_map(board_size)
        for row in range(0, board_size):
            for column in range(0, board_size):
                self.assertFalse(game_map[row][column]["is_revealed"])

    def test_generate_board(self):
        game_map = self.game.get_game_map()
        game_board = self.game.get_game_board()
        self.assertEqual(generate_board(game_map), game_board)

    def test_get_adjacent_cells(self):
        game_map = self.game.get_game_map()
        self.assertEqual(
            generate_adjacent_cells(0, 0, game_map), [(0, 1), (1, 0), (1, 1)]
        )
        self.assertEqual(
            generate_adjacent_cells(1, 0, game_map),
            [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)],
        )
        self.assertEqual(
            generate_adjacent_cells(1, 1, game_map),
            [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
        )


class TestUtilMethods(unittest.TestCase):
    def setUp(self):
        self.decoded_string = "1"
        self.encoded_string = "MQ"

    def test_encode(self):
        encoded_string = encode(self.decoded_string)
        self.assertEqual(self.encoded_string, encoded_string)
        decoded_string = decode(encoded_string)
        self.assertEqual(self.decoded_string, decoded_string)
