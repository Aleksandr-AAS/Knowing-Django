from django.views.generic import ListView, DetailView, TemplateView
from .models import Product


# ========== CBV: Главная страница (список товаров) ==========
class HomeView(ListView):
    """
    Контроллер для главной страницы.
    Отображает список всех товаров.
    """

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"
    ordering = ["-created_at"]


# ========== CBV: Детальная страница товара ==========
class ProductDetailView(DetailView):
    """
    Контроллер для детальной страницы товара.
    Отображает полную информацию о конкретном товаре.
    """

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        """
        Добавляем похожие товары в контекст (по желанию)
        """
        context = super().get_context_data(**kwargs)
        # Получаем текущий товар
        current_product = self.get_object()
        # Ищем похожие товары из той же категории, исключая текущий
        context["similar_products"] = Product.objects.filter(
            category=current_product.category
        ).exclude(pk=current_product.pk)[:4]
        return context


# ========== CBV: Страница контактов ==========
class ContactsView(TemplateView):
    """
    Контроллер для страницы контактов.
    TemplateView просто отображает шаблон без дополнительных данных.
    """

    template_name = "catalog/contacts.html"

    # Опционально: можно добавить контекстные данные
    def get_context_data(self, **kwargs):
        """
        Добавляем контактные данные в контекст (вместо жесткого кода в шаблоне)
        """
        context = super().get_context_data(**kwargs)
        context["phone"] = "+7 (495) 123-45-67"
        context["email"] = "info@catalog.ru"
        context["address"] = "г. Москва, ул. Тверская, д. 1"
        context["work_hours"] = "Пн-Пт: 9:00 - 20:00, Сб-Вс: 10:00 - 18:00"
        return context
