from django.shortcuts import render

# Create your views here.
def home_view(request):
    return render(request, "home.html", {})


def legal_view(request):
    return render(request, "legal.html", {})


def about_view(request):
    return render(request, "about.html", {})
