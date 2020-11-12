from django.shortcuts import render


# Create your views here.

def homepage_view(request):
    return render(request, "base/homepg1.html")


def register_view(request):
    return render(request, "base/register.html")


def login_view(request):
    return render(request, "base/login.html")
