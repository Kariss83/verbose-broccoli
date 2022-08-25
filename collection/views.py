from django.shortcuts import render, redirect
from django.views import generic

from .models import Game

class GameListView(generic.ListView):
    model = Game

    context_object_name = 'games_list'

    template_name = 'games/game_list.html'


class GameDetailView(generic.ListView):
    model = Game

    context_object_name = 'games'

    template_name = 'games/game_detail.html'
