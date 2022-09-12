# Django
from django.urls import path

# local Django
from . import views


app_name = "barcode"

urlpatterns = [
    path("upload/", views.upload_barcode, name="upload"),
]
