from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Game, Collection


class GameListView(generic.ListView):
    model = Game

    context_object_name = 'games_list'

    template_name = 'games/game_list.html'


class GameDetailView(generic.ListView):
    model = Game

    context_object_name = 'games'

    template_name = 'games/game_detail.html'

@login_required
def add_game_to_collection(request):
    if request.method == 'POST':
        print(request.POST)
        collection_name = request.POST.get('collections', '')
        collection = Collection.objects.get(name=collection_name)
        barcode = request.POST.get('barcode', '')
        game = Game.objects.get(barcode=barcode)
        collection.games.add(game)
        all_games_in_collection = collection.games.all()
        messages.success(request, (f'{game.name} have been added to your collection'))
        

        context = {'collection': collection,
                   'games': all_games_in_collection}

    return render(
            request,
            'collections/my_collections.html',
            context
            )