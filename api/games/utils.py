import base64


def encode(string):
    return base64.urlsafe_b64encode(string.encode()).rstrip(b"=").decode("utf-8")


def decode(encoded_string):
    padded_encoded_string = encoded_string + "=="[: (len(encoded_string) % 4)]
    return base64.urlsafe_b64decode(padded_encoded_string).decode()


def stringify_game_map(game_map):
    json_game_map = {}
    for row_index, row in game_map.items():
        str_row_index = str(row_index)
        json_game_map[str_row_index] = {}
        for column_index, cell in row.items():
            str_column_index = str(column_index)
            json_game_map[str_row_index][str_column_index] = cell

    return json_game_map


def parse_json_game_map(json_game_map):
    parsed = {}
    for str_row_index, row in json_game_map.items():
        row_index = int(str_row_index)
        parsed[row_index] = {}
        for str_column_index, cell in row.items():
            column_index = int(str_column_index)
            parsed[row_index][column_index] = cell

    return parsed


def visualize_game(game):
    generate_board(game.game_map)
