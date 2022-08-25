from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'collection'

urlpatterns = [
    path('games/', views.GameListView.as_view(), name='games'),
    path('games/<int:barcode>', views.GameDetailView.as_view(), name='game_detail'),
]
