import unittest

from django.test import TestCase
from games.services.boards import (
    generate_board,
    generate_map,
    generate_adjacent_cells,
    calculate_board_cell_value,
    update_game_map,
)
from games.utils import encode, decode, parse_json_game_map, stringify_game_map


class TestGame:
    """
    # game_map visualization:
    T  F  F
    T  F  F
    F  F  F

    # game_board visualizaton:
    -1 2  0
    -1 2  0
    1  1  0

    """

    def __init__(self):
        self.__game_map = {
            0: {
                0: {"is_bomb": True, "is_revealed": False},
                1: {"is_bomb": False, "is_revealed": False},
                2: {"is_bomb": False, "is_revealed": False},
            },
            1: {
                0: {"is_bomb": True, "is_revealed": False},
                1: {"is_bomb": False, "is_revealed": False},
                2: {"is_bomb": False, "is_revealed": False},
            },
            2: {
                0: {"is_bomb": False, "is_revealed": False},
                1: {"is_bomb": False, "is_revealed": False},
                2: {"is_bomb": False, "is_revealed": False},
            },
        }
        self.__game_board = [None, None, None, None, None, None, None, None, None]

    def get_game_map(self):
        return self.__game_map

    def get_game_board(self):
        return self.__game_board


class TestBoardMethods(unittest.TestCase):
    def setUp(self):
        self.game = TestGame()

    def test_calculate_cell_value_in_board(self):
        game_map = self.game.get_game_map()
        # if it is not revealed: default None
        self.assertEqual(calculate_board_cell_value(0, 0, game_map), None)
        self.assertEqual(calculate_board_cell_value(0, 1, game_map), None)
        # if it is not revealed with no masking arg: check adjacent cells
        self.assertEqual(calculate_board_cell_value(1, 1, game_map, False), 2)
        # if it is revealed and is a bomb: -1
        game_map[1][0]["is_revealed"] = True
        self.assertEqual(calculate_board_cell_value(1, 0, game_map), -1)
        # if it is is revealed and not a bomb: check adjacent cells
        game_map[1][1]["is_revealed"] = True
        game_map[2][2]["is_revealed"] = True
        self.assertEqual(calculate_board_cell_value(1, 1, game_map), 2)
        self.assertEqual(calculate_board_cell_value(2, 2, game_map), 0)

    def test_generate_map_size(self):
        board_size = 3
        game_map = generate_map(board_size)
        self.assertEqual(len(game_map.keys()), board_size)
        self.assertEqual(len(game_map[0].keys()), board_size)

    def test_generate_map_initial_values(self):
        game_map = generate_map()
        for row in range(len(game_map.keys())):
            for column in range(len(game_map.keys())):
                self.assertFalse(game_map[row][column]["is_revealed"])

    def test_generate_board(self):
        game_map = self.game.get_game_map()
        game_board = self.game.get_game_board()
        self.assertEqual(generate_board(game_map), game_board)

        # reveal certain cells
        game_map[1][0]["is_revealed"] = True  # bomb
        game_map[1][1]["is_revealed"] = True  # value == 2
        game_map[2][2]["is_revealed"] = True  # value == 0
        game_board[3] = -1
        game_board[4] = 2
        game_board[8] = 0
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

    """
    # game update:
    N   N  N       N  N  N
    -1 (2) N  =>  -1  2  N 
    N   N  N       N  N  N
    
    """

    def test_update_board_clicking_revealed_cell(self):
        game_map = self.game.get_game_map()
        updated_game_map = update_game_map(1, 1, game_map)
        self.assertEqual(updated_game_map, game_map)

    """
    # game update:
    (N) N  N      -1  N  N
    -1  2  N  =>  -1  2  N 
    N   N  N       N  N  N
    
    """

    def test_update_board_clicking_bomb(self):
        game_map = self.game.get_game_map()
        updated_game_map = update_game_map(0, 0, game_map)
        self.assertEqual(
            updated_game_map[0][0],
            dict(is_bomb=True, is_revealed=True),
        )
        for row in range(3):
            for column in range(3):
                if row != 0 and column != 0:
                    self.assertEqual(
                        updated_game_map[row][column],
                        game_map[row][column],
                    )

    """
    # game update:
    N  (N)  N     N   2  N
    -1  2   N  => -1  2  N 
    N   N   N     N   N  N
    
    """

    def test_update_board_clicking_single_update(self):
        game_map = self.game.get_game_map()
        updated_game_map = update_game_map(0, 1, game_map)
        self.assertEqual(
            updated_game_map[0][1],
            dict(is_bomb=False, is_revealed=True),
        )
        for row in range(3):
            for column in range(3):
                if row != 0 and column != 1:
                    self.assertEqual(
                        updated_game_map[row][column],
                        game_map[row][column],
                    )

    """
    # game update:
    N   N   N      N   2   0
    -1  2   N  => -1   2   0 
    N   N  (N)     N   1   0
    
    """

    def test_update_board_clicking_multiple_updates(self):
        game_map = self.game.get_game_map()
        updated_game_map = update_game_map(2, 2, game_map)
        for row in range(3):
            for column in range(3):
                if column != 0:
                    self.assertTrue(updated_game_map[row][column]["is_revealed"])
                else:
                    self.assertEqual(
                        updated_game_map[row][column],
                        game_map[row][column],
                    )


class TestUtilMethods(unittest.TestCase):
    def setUp(self):
        self.decoded_string = "1"
        self.encoded_string = "MQ"

    def test_encode(self):
        encoded_string = encode(self.decoded_string)
        self.assertEqual(self.encoded_string, encoded_string)


class TestUtilMethods(unittest.TestCase):
    def setUp(self):
        self.decoded_string = "1"
        self.encoded_string = "MQ"

    def test_encode(self):
        encoded_string = encode(self.decoded_string)
        self.assertEqual(self.encoded_string, encoded_string)

    def test_decode(self):
        decoded_string = decode(self.encoded_string)
        self.assertEqual(self.decoded_string, decoded_string)

    def test_parse_json_map(self):
        game_map = {
            0: {
                0: dict(is_bomb=False, is_complete=False),
                1: dict(is_bomb=False, is_complete=False),
            }
        }
        json_game_map = {
            "0": {
                "0": dict(is_bomb=False, is_complete=False),
                "1": dict(is_bomb=False, is_complete=False),
            }
        }
        self.assertEqual(game_map, parse_json_game_map(json_game_map))
        self.assertEqual(json_game_map, stringify_game_map(game_map))
