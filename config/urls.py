"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from gamezscan.home import views as home_views
import gamezscan.accounts.urls
import gamezscan.barcode.urls
import gamezscan.collection.urls
import gamezscan.datafetcher.urls

urlpatterns = [
    path("", home_views.home_view, name="home"),
    path("about", home_views.about_view, name="about"),
    path("legal", home_views.legal_view, name="legal"),
    path("__debug__/", include("debug_toolbar.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include(gamezscan.accounts.urls, namespace="accounts")),
    path("barcode/", include(gamezscan.barcode.urls, namespace="barcode")),
    path("collection/", include(gamezscan.collection.urls, namespace="collection")),
    path("datafetcher/", include(gamezscan.datafetcher.urls, namespace="datafetcher")),
]

handler404 = "gamezscan.home.views.entry_not_found"
handler500 = "gamezscan.home.views.internal_error"
