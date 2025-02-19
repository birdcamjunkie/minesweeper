from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from games.models import Game
from games.constants import UNREVEALED_BOARD_CELL_VALUE, BOARD_BOMB_VALUE
from games.utils import encode, decode
from games.services.boards import generate_map, generate_board, update_board
from django.core.exceptions import ObjectDoesNotExist

# TODO: remove
@csrf_exempt
def create_game(request, *args, **kwargs):
    if request.method == "POST":
        new_map = generate_map();
        new_game = Game.objects.create(values=new_map)
        new_board = generate_board(new_game.values)

        return JsonResponse(dict(id=new_game_alias, is_complete=new_game.is_complete, game_board=new_board))
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
            board = generate_board(game.values)
            return JsonResponse(dict(id=game_id, is_complete=game.is_complete, game_board=board)) 
    else:
        return HttpResponseNotAllowed("Method not supported")

def update_game(request, game_id, grid_id, *args, **kwargs):
    if request.method == "PUT":
        try:
            game = Game.objects.get(id=decode(game_id))
        except:
            return HttpResponseBadRequest()
        if game is None:
            return HttpResponseBadRequest()
        else:
            # TODO: remove stub and get it from the body
            # also validate we only get one move at a time
            row_index = 0 
            column_index = 0
            board = update_board(row_index, column_index, game.id)
            return HttpResponse(board)
    else:
        return HttpResponseNotAllowed("Method not supported")
