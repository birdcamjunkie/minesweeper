import random
from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
    JsonResponse,
)
from django.views.decorators.csrf import csrf_exempt
from games.models import Game
from games.constants import (
    UNREVEALED_BOARD_CELL_VALUE,
    BOARD_BOMB_VALUE,
    BOARD_WIDTH,
    BOARD_BOMB_PERCENTAGE,
)
from games.utils import encode, decode, parse_json_game_map, stringify_game_map


def generate_map(size=BOARD_WIDTH):
    game_map = {}
    for row_index in range(0, size):
        columns = {}
        for column in range(0, size):
            is_bomb = random.randint(1, 100) <= BOARD_BOMB_PERCENTAGE
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


# TODO: game_map arg may not be necessary - remove
def generate_adjacent_cells(row_index, column_index, game_map):
    size = len(game_map.keys())
    adjacent_cells = [
        (row, column)
        for row in range(row_index - 1, row_index + 2)
        for column in range(column_index - 1, column_index + 2)
        if 0 <= row < size
        if 0 <= column < size
        if not (row == row_index and column == column_index)
    ]
    return adjacent_cells


def calculate_board_cell_value(
    row_index, column_index, game_map, mask_hidden_cell_value=True
):
    cell = game_map[row_index][column_index]
    if mask_hidden_cell_value and not cell["is_revealed"]:
        return UNREVEALED_BOARD_CELL_VALUE
    else:
        if cell["is_bomb"]:
            return BOARD_BOMB_VALUE
        else:
            cell_value = 0
            adjacent_cells = generate_adjacent_cells(row_index, column_index, game_map)
            for row, column in adjacent_cells:
                if game_map[row][column]["is_bomb"]:
                    cell_value += 1

            return cell_value


def update_game(row_index, column_index, game):
    game_map = parse_json_game_map(game.game_map)
    # no need to update a game if it is completed already
    if game.is_complete:
        game_board = generate_board(game_map)
        return dic(
            id=encode(str(game.id)), is_complete=game.is_complete, game_board=game_board
        )
    else:
        updated_game_map = update_game_map(row_index, column_index, game_map)
        clicked_bombs = [
            cell
            for row in game_map.values()
            for cell in row.values()
            if cell["is_bomb"] and cell["is_revealed"]
        ]
        unclicked_regular_cells = [
            cell
            for row in updated_game_map.values()
            for cell in row.values()
            if not cell["is_bomb"] and not cell["is_revealed"]
        ]
        game.is_complete = len(clicked_bombs) > 0 or len(unclicked_regular_cells) == 0
        game.game_map = stringify_game_map(updated_game_map)
        game.save()

        return dict(
            id=encode(str(game.id)),
            is_complete=game.is_complete,
            game_board=generate_board(parse_json_game_map(game.game_map)),
        )


def update_game_map(row_index, column_index, game_map):
    is_bomb, is_revealed = game_map[row_index][column_index].values()
    if not is_revealed:
        if is_bomb:
            game_map[row_index][column_index]["is_revealed"] = True
        else:
            cells_to_update = [(row_index, column_index)]
            while len(cells_to_update) > 0:
                (row, column) = cells_to_update.pop()
                game_map[row][column]["is_revealed"] = True
                cell_value = calculate_board_cell_value(row, column, game_map, False)
                if cell_value == 0:
                    for i, j in generate_adjacent_cells(row, column, game_map):
                        is_bomb, is_revealed = game_map[i][j].values()
                        if not is_bomb and not is_revealed:
                            cells_to_update.append((i, j))

    return game_map
