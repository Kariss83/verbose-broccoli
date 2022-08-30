from django.urls import path

from . import views

app_name = 'collection'

urlpatterns = [
    path('games/', views.GameListView.as_view(), name='games'),
    path('games/<int:barcode>', views.GameDetailView.as_view(), name='game_detail'),
    path('add_game', views.add_game_to_collection, name='add_game_to_collection'),
    path('all', views.see_all_collections, name='all_collections'),
    path('create', views.create_new_collection, name='create')
]
