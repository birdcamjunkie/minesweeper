from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseNotAllowed, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from games.models import Game

@csrf_exempt
def create_game(request, *args, **kwargs):
    if request.method == "POST":
        new_board = {
            0: { 'is_bomb': True, 'is_revealed': False },
            1: { 'is_bomb': False, 'is_revealed': False },
            2: { 'is_bomb': False, 'is_revealed': False },
            3: { 'is_bomb': False, 'is_revealed': False },
            4: { 'is_bomb': False, 'is_revealed': False },
            5: { 'is_bomb': False, 'is_revealed': False },
            6: { 'is_bomb': False, 'is_revealed': False },
            7: { 'is_bomb': False, 'is_revealed': False },
            8: { 'is_bomb': False, 'is_revealed': False },
        }
        new_game = Game.objects.create(values=new_board)
        return HttpResponse(new_board)
    else:
        raise HttpResponseNotAllowed("Method not supported")

def get_game(request, game_id, *args, **kwargs):
    if request.method == "GET":
        game = Game.objects.get(id=game_id)
        ## TODO: algo to transform raw game into a board with value
        return HttpResponse({
                'game_id': game.id,
                'is_complete': game.is_complete,
                'values': [None, 1, None, None, None, None, None, None, None]
            }) 
    else:
        raise HttpResponseNotAllowed("Method not supported")

def update_game(request, game_id, grid_id, *args, **kwargs):
    ## Has to be a put request
    return HttpResponse('')
