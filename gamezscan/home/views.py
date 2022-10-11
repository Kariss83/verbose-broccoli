from django.shortcuts import render

# Create your views here.
def home_view(request):
    return render(request, "home.html", {})


def legal_view(request):
    return render(request, "legal.html", {})


def about_view(request):
    return render(request, "about.html", {})


def entry_not_found(request, exception, template_name="404.html"):
    return render(request, template_name)


def internal_error(request, template_name="500.html"):
    return render(request, template_name)
