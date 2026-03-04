from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Добро пожаловать в каталог!")


# from django.shortcuts import render


def home(request):
    return render(request, "catalog/home.html")


def contacts(request):
    return render(request, "catalog/contacts.html")
