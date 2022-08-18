from django.urls import path
from django.contrib.auth import views as auth_views #import this

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('edit/', views.edit_profile, name='edit'),
    path('password_reset/', views.password_reset_request, name="password_reset"),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='passwords/password_reset_done.html'),
        name='password_reset_done'),
    path(
        'reset/<uidb64>/<token>/',
        views.CustomPasswordResetConfirmView.as_view(template_name="passwords/password_reset_confirm.html"),
        name='password_reset_confirm'),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='passwords/password_reset_complete.html'),
        name='password_reset_complete'),
]