from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.shortcuts import get_object_or_404, redirect
from django.core.cache import cache
from django.conf import settings
from .models import Product
from .forms import ProductForm
from .services import (
    get_products_by_category,
    get_category_by_id,
    get_all_categories,
    clear_category_cache,
)


# ========== Публичные контроллеры (доступны всем) ==========


class HomeView(ListView):
    """
    Главная страница - список опубликованных товаров с низкоуровневым кешированием
    """

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        # Проверяем, включено ли кеширование
        if not getattr(settings, "CACHE_ENABLED", True):
            return Product.objects.filter(is_published=True).order_by("-created_at")

        # Ключ для кеша
        cache_key = getattr(settings, "CACHE_KEYS", {}).get(
            "home_products", "home_products_list"
        )
        timeout = getattr(settings, "CACHE_TIMEOUTS", {}).get("home_page", 60 * 5)

        # Пытаемся получить данные из кеша
        products = cache.get(cache_key)

        if products is None:
            # Данных нет в кеше - делаем запрос к БД
            products = list(
                Product.objects.filter(is_published=True)
                .select_related("category", "owner")
                .order_by("-created_at")
            )
            # Сохраняем в кеш
            cache.set(cache_key, products, timeout)

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем категории в контекст
        context["categories"] = get_all_categories()
        return context


class ProductDetailView(DetailView):
    """
    Детальная страница товара
    """

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        if self.request.user.has_perm("catalog.can_unpublish_product"):
            return Product.objects.all()
        return Product.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем похожие товары
        context["similar_products"] = Product.objects.filter(
            category=self.object.category, is_published=True
        ).exclude(pk=self.object.pk)[:4]
        return context


class ContactsView(TemplateView):
    """
    Страница контактов
    """

    template_name = "catalog/contacts.html"


class CategoryProductsView(ListView):
    """
    Страница товаров в категории
    """

    model = Product
    template_name = "catalog/category_products.html"
    context_object_name = "products"
    paginate_by = 12

    def dispatch(self, request, *args, **kwargs):
        # Получаем категорию по id
        self.category = get_category_by_id(self.kwargs.get("pk"))
        if not self.category:
            messages.error(request, "Категория не найдена")
            return redirect("catalog:home")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Используем сервисную функцию
        return get_products_by_category(self.category.id, published_only=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        context["title"] = f"Товары в категории: {self.category.name}"
        return context


# ========== Контроллеры для управления продуктами (только для авторизованных) ==========


class ProductListView(LoginRequiredMixin, ListView):
    """
    Список товаров для управления
    """

    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.has_perm("catalog.can_unpublish_product"):
            return Product.objects.all().order_by("-created_at")
        return Product.objects.filter(owner=user).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_user"] = self.request.user
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Создание товара - автоматически назначается владелец
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
        # Автоматически привязываем продукт к текущему пользователю
        form.instance.owner = self.request.user
        response = super().form_valid(form)

        # Очищаем кеш главной страницы
        cache_key = getattr(settings, "CACHE_KEYS", {}).get(
            "home_products", "home_products_list"
        )
        cache.delete(cache_key)

        # Очищаем кеш категории товара
        clear_category_cache(form.instance.category_id)

        messages.success(self.request, "Товар успешно создан!")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Исправьте ошибки в форме.")
        return super().form_invalid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Редактирование товара - только владелец или модератор
    """

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_success_url(self):
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование товара"
        context["button_text"] = "Сохранить изменения"
        return context

    def test_func(self):
        """Проверка: только владелец или модератор могут редактировать"""
        product = self.get_object()
        user = self.request.user
        return product.is_owner(user) or user.has_perm("catalog.can_unpublish_product")

    def form_valid(self, form):
        response = super().form_valid(form)

        # Очищаем кеш главной страницы
        cache_key = getattr(settings, "CACHE_KEYS", {}).get(
            "home_products", "home_products_list"
        )
        cache.delete(cache_key)

        # Очищаем кеш категории товара
        clear_category_cache(self.object.category_id)

        messages.success(self.request, "Товар успешно обновлен!")
        return response

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для редактирования этого товара.")
        return redirect("catalog:product_list")


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Удаление товара - владелец или модератор
    """

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:product_list")

    def test_func(self):
        """Проверка: владелец или модератор могут удалять"""
        product = self.get_object()
        user = self.request.user
        return product.can_delete(user)

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        category_id = product.category_id

        # Очищаем кеш главной страницы
        cache_key = getattr(settings, "CACHE_KEYS", {}).get(
            "home_products", "home_products_list"
        )
        cache.delete(cache_key)

        # Очищаем кеш категории товара
        clear_category_cache(category_id)

        messages.success(request, "Товар успешно удален!")
        return super().delete(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для удаления этого товара.")
        return redirect("catalog:product_list")


class ProductTogglePublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Переключение статуса публикации - только для модераторов
    """

    permission_required = "catalog.can_unpublish_product"

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = not product.is_published
        product.save()

        # Очищаем кеш главной страницы
        cache_key = getattr(settings, "CACHE_KEYS", {}).get(
            "home_products", "home_products_list"
        )
        cache.delete(cache_key)

        # Очищаем кеш категории товара
        clear_category_cache(product.category_id)

        status = "опубликован" if product.is_published else "снят с публикации"
        messages.success(request, f'Товар "{product.name}" успешно {status}.')
        return redirect("catalog:product_list")
