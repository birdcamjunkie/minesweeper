from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
    HttpResponseNotFound,
    JsonResponse,
)
from django.views.decorators.csrf import csrf_exempt
from games.models import Game
from games.constants import BOARD_WIDTH
from games.utils import encode, decode, parse_json_game_map
from games.services.boards import generate_map, generate_board, update_game
from django.core.exceptions import ObjectDoesNotExist


# TODO: remove csrf policy
@csrf_exempt
def create_game(request, *args, **kwargs):
    if request.method == "POST":
        new_map = generate_map()
        new_game = Game.objects.create(game_map=new_map)
        new_board = generate_board(new_game.game_map)
        new_game_alias = encode(str(new_game.id))

        return JsonResponse(
            dict(
                id=new_game_alias,
                is_complete=new_game.is_complete,
                game_board=new_board,
            )
        )
    else:
        return HttpResponseNotAllowed("Method not supported")


def get_game(request, game_id, *args, **kwargs):
    if request.method == "GET":
        try:
            game = Game.objects.get(id=decode(game_id))
            if game is None:
                raise ObjectDoesNotExist()
        except:
            return HttpResponseNotFound()
        else:
            board = generate_board(parse_json_game_map(game.game_map))
            return JsonResponse(
                dict(id=game_id, is_complete=game.is_complete, game_board=board)
            )
    else:
        return HttpResponseNotAllowed("Method not supported")


@csrf_exempt
def update_cell(request, game_id, cell_id, *args, **kwargs):
    if request.method == "PUT":
        try:
            game = Game.objects.get(id=decode(game_id))
            if game is None:
                raise ObjectDoesNotExist()
            else:
                row_index, column_index = divmod(cell_id, BOARD_WIDTH)
                if (not (0 <= row_index < BOARD_WIDTH)) or (
                    not (0 <= column_index < BOARD_WIDTH)
                ):
                    raise ObjectDoesNotExist()

                updated_game = update_game(row_index, column_index, game)
                return JsonResponse(updated_game)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest()
    else:
        return HttpResponseNotAllowed("Method not supported")
