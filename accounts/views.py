# Create your views here.
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.views import PasswordResetConfirmView

from collection.models import Collection
from accounts.models import CustomUser
from accounts.forms import CustomPasswordResetForm
from accounts.forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    CustomUserChangeForm,
)


# login view
def login_user(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST.get("email", "")
            password = request.POST.get("password", "")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, ("You are logged in !"))
                return redirect("/")
            else:
                messages.error(
                    request,
                    'Connexion error ("Bad informations") - Try again...',
                )
                return redirect("/accounts/login")
        else:
            errors = form.errors
            messages.error(request, (f"Connexion error ({errors}) - Try again..."))
            return redirect("/accounts/login")
    else:
        return render(
            request, "accounts/login.html", {"form": CustomAuthenticationForm()}
        )


# logout view
@login_required
def logout_user(request):
    logout(request)
    messages.success(request, ("You are disconnected..."))
    return redirect("/")


# register view
def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            form.save()
            user = authenticate(email=email, password=password)
            if user is not None:
                Collection.objects.create(name="My First Collection", user=user)
                login(request, user)
                messages.success(request, ("You are now signed in..."))
                return redirect("/accounts/profile")
        else:
            errors = form.errors
            messages.error(
                request, (f"Account creation error ({errors})- Try Again...")
            )
            return redirect("/accounts/register")
    else:
        form = CustomUserCreationForm()
        context = {"form": form}
        return render(request, "accounts/register.html", context)


# profile view
@login_required
def profile(request):
    return render(request, "accounts/profile.html", {})


# edit profile view
@login_required
def edit_profile(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ("Modification successfully saved"))
            return redirect("/accounts/profile")
        else:
            messages.error(
                request, ("There was an error in the form you filled, try again.")
            )
            return redirect("/accounts/edit")
    else:
        form = CustomUserChangeForm(instance=request.user)
        context = {"form": form}
        return render(request, "accounts/edit_profile.html", context)


class HomeView(TemplateView):
    template_name = "home/index.html"


class LegalView(TemplateView):
    template_name = "home/legal.html"


# password reset request view
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = CustomPasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data["email"]
            associated_users = CustomUser.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "passwords/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        "domain": "127.0.0.1:8000",
                        "site_name": "GameZScan",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(
                            subject,
                            email,
                            "root@vps-8351387e.vps.ovh.net",
                            [user.email],
                            fail_silently=False,
                        )
                    except BadHeaderError:
                        return HttpResponse("Invalid header found.")
                    return redirect("/accounts/password_reset/done")
            else:
                messages.error(request, "This email is invalid.")
                return redirect("/accounts/password_reset")
    else:
        password_reset_form = CustomPasswordResetForm()
        return render(
            request,
            "passwords/password_reset.html",
            {"password_reset_form": password_reset_form},
        )


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("accounts:password_reset_complete")
