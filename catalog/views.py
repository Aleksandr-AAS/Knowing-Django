from django.shortcuts import render, get_object_or_404
from .models import Product


def home(request):
    """
    Главная страница каталога со списком товаров
    """

    products = Product.objects.all().order_by("-created_at")

    context = {"products": products}
    return render(request, "catalog/home.html", context)


def contacts(request):
    return render(request, "catalog/contacts.html")


def product_detail(request, pk):
    """
    Отображает страницу с подробной информацией о товаре
    """
    # Ищем товар по id в базе данных
    # Если товар не найден — автоматически вернется 404 ошибка
    product = get_object_or_404(Product, id=pk)

    # Передаем найденный товар в шаблон
    context = {"product": product}
    return render(request, "catalog/product_detail.html", context)
