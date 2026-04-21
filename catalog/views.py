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
from .models import Product
from .forms import ProductForm


# ========== Публичные контроллеры ==========


class HomeView(ListView):
    """
    Главная страница - только опубликованные товары
    """

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(is_published=True).order_by("-created_at")


class ProductDetailView(DetailView):
    """
    Детальная страница товара
    """

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        # Модераторы видят все товары, остальные только опубликованные
        if self.request.user.has_perm("catalog.can_unpublish_product"):
            return Product.objects.all()
        return Product.objects.filter(is_published=True)


class ContactsView(TemplateView):
    """
    Страница контактов
    """

    template_name = "catalog/contacts.html"


# ========== Контроллеры для управления продуктами ==========
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
        # Добавляем текущего пользователя в контекст для проверок в шаблоне
        context["current_user"] = self.request.user
        return context


# class ProductListView(LoginRequiredMixin, ListView):
#     """
#     Список товаров для управления
#     """
#     model = Product
#     template_name = 'catalog/product_list.html'
#     context_object_name = 'products'
#     paginate_by = 10
#
#     def get_queryset(self):
#         user = self.request.user
#         # Модераторы видят все товары, обычные пользователи только свои
#         if user.has_perm('catalog.can_unpublish_product'):
#             return Product.objects.all().order_by('-created_at')
#         return Product.objects.filter(owner=user).order_by('-created_at')


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
        # ✅ Автоматически привязываем продукт к текущему пользователю
        form.instance.owner = self.request.user
        messages.success(self.request, "Товар успешно создан!")
        return super().form_valid(form)

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

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для редактирования этого товара.")
        return redirect("catalog:product_list")

    def form_valid(self, form):
        messages.success(self.request, "Товар успешно обновлен!")
        return super().form_valid(form)


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

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для удаления этого товара.")
        return redirect("catalog:product_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Товар успешно удален!")
        return super().delete(request, *args, **kwargs)


class ProductTogglePublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Переключение статуса публикации - только для модераторов
    """

    permission_required = "catalog.can_unpublish_product"

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = not product.is_published
        product.save()

        status = "опубликован" if product.is_published else "снят с публикации"
        messages.success(request, f'Товар "{product.name}" успешно {status}.')
        return redirect("catalog:product_list")
