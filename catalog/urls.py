from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # главная страница (первый вариант)
    path("contacts/", views.contacts, name="contacts"),  # страница контактов
    path(
        "product/<int:pk>/", views.product_detail, name="product_detail"
    ),  # детальная страница товара
]
