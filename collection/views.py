from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import IntegrityError, transaction
from django.core.exceptions import PermissionDenied

from .models import Game, Collection
from .forms import CreateCollectionForm


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
                'collections/my_collection.html',
                context
                )
    else:
        raise PermissionDenied()


@login_required
def see_all_collections(request):
    user = request.user
    collections = Collection.objects.filter(user=user)
    game_collection = []
    for collection in collections:
        collection_info = {'name': collection.name,
                           'game_list': collection.games.all(),
                           'value': collection._return_total_value()}
        game_collection.append(collection_info)
    context = {'game_collection': game_collection}
    return render(
            request,
            'collections/all_collections.html',
            context
            )


@login_required
@transaction.atomic
def create_new_collection(request):
    if request.method == 'POST':
        form = CreateCollectionForm(request.POST)
        collection_name = request.POST.get('name', '')
        try:
            with transaction.atomic():
                Collection.objects.create(name=collection_name, user=request.user)
                return redirect('/collection/all')
        except IntegrityError:
            messages.error(request, 'You already have a collection with that name')
            return redirect('/collection/create')

    else:
        form = CreateCollectionForm()
        return render(request, 'collections/create_new.html', {'form': form})


@login_required
def delete_collection(request):
    if request.method == 'POST':
        collection_name = request.POST.get('collection', '')
        user = request.user
        Collection.objects.get(user=user, name=collection_name).delete()
        return redirect('collection:all_collections')
    else:
        raise PermissionDenied()


@login_required
def remove_from_collection(request):
    if request.method == 'POST':
        collection_name = request.POST.get('collection', '')
        game_barcode = request.POST.get('barcode', '')
        user = request.user
        collection = Collection.objects.get(
            user=user,
            name=collection_name
        )
        game = Game.objects.get(barcode=game_barcode)
        collection.games.remove(game)
        return redirect('collection:all_collections')
    else:
        raise PermissionDenied()
