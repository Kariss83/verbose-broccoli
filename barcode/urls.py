from django.urls import path
from django.contrib.auth import views as auth_views #import this

from . import views

app_name = 'barcode'

urlpatterns = [
    path('upload/', views.upload_barcode, name='upload'),
]