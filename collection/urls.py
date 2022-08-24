from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'collection'

urlpatterns = [
    path('scan/', views.scan_barcode, name='scan'),
]
