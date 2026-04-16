from django.views.generic import TemplateView
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Product
from .forms import ProductForm


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


class ProductCreateView(CreateView):
    """
    Контроллер для создания нового товара
    """

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:product_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавление товара"
        context["button_text"] = "Создать товар"
        return context

    def form_valid(self, form):
        """Дополнительная логика при успешном создании"""
        messages.success(self.request, "Товар успешно создан!")
        return super().form_valid(form)

    def form_invalid(self, form):
        """Логика при невалидной форме"""
        messages.error(self.request, "Исправьте ошибки в форме.")
        return super().form_invalid(form)


class ProductUpdateView(UpdateView):
    """
    Контроллер для редактирования товара
    """

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_success_url(self):
        """После успешного редактирования перенаправляем на детальную страницу"""
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование товара"
        context["button_text"] = "Сохранить изменения"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Товар успешно обновлен!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Исправьте ошибки в форме.")
        return super().form_invalid(form)


class ProductDeleteView(DeleteView):
    """
    Контроллер для удаления товара
    """

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:product_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Товар успешно удален!")
        return super().delete(request, *args, **kwargs)


class ProductListView(ListView):
    """
    Контроллер для списка всех товаров (для управления)
    """

    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        """Можно добавить фильтрацию, сортировку"""
        return Product.objects.all().order_by("-created_at")
