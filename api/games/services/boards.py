import random
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from games.models import Game
from games.constants import UNREVEALED_BOARD_CELL_VALUE, BOARD_BOMB_VALUE
from games.utils import encode, decode
from games.constants import BOARD_WIDTH, BOARD_BOMB_PERCENTAGE

def generate_map(size=BOARD_WIDTH):
    game_map = {}
    for row_index in range(0, size):
        columns = {}
        for column in range(0, size):
            is_bomb = random.randint(1,100) <= BOARD_BOMB_PERCENTAGE
            columns[column] = dict(is_bomb=is_bomb, is_revealed=False) 
        game_map[row_index] = columns
    return game_map


def generate_board(game_map):
    board = [
            calculate_board_cell_value(row_index, column_index, game_map)
            for row_index, row in game_map.items()
            for column_index, cell in row.items()
    ]
    return board


def generate_adjacent_cells(row_index, column_index, game_map):
    adjacent_cells = [
        (row, column)
        for row in range(row_index - 1, row_index + 2)
        for column in range(column_index - 1, column_index + 2)
        if row in game_map.keys()
        if column in game_map[0].keys() 
        if not (row == row_index and column == column_index)
    ]
    return adjacent_cells


def calculate_board_cell_value(row_index, column_index, game_map):
    cell = game_map[row_index][column_index]
    if not cell['is_revealed']:
        return UNREVEALED_BOARD_CELL_VALUE
    else:
        if cell['is_bomb']:
            return BOARD_BOMB_VALUE;
        else:
            cell_value = 0
            adjacent_cells = generate_adjacent_cells(row_index, column_index, game_map)
            for (row, column) in adjacent_cells:
                if game_map[row][column]['is_bomb']:
                    cell_value += 1

            return cell_value;

def update_board(row_index, column_index, game_map):
    return ''
