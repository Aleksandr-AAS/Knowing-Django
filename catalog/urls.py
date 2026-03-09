from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
]


urlpatterns = [
    path("", views.home, name="home"),  # главная страница каталога
    path("contacts/", views.contacts, name="contacts"),  # страница контактов
]
