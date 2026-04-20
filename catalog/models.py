from django.db import models
from django.urls import reverse
from django.conf import settings


class Category(models.Model):
    """
    Модель категории товаров
    """

    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", blank=True)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Модель продукта с полем статуса публикации и владельцем
    """

    name = models.CharField(max_length=200, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", blank=True)
    image = models.ImageField(
        upload_to="products/", verbose_name="Изображение", blank=True, null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    # Поле владельца продукта
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Владелец",
        null=True,
        blank=True,
    )

    # Поле статуса публикации
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        ordering = ["-created_at"]

        # Кастомные права
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:product_detail", kwargs={"pk": self.pk})

    def is_owner(self, user):
        """Проверяет, является ли пользователь владельцем продукта"""
        return user.is_authenticated and self.owner == user

    def can_edit(self, user):
        """Проверяет, может ли пользователь редактировать продукт"""
        return self.is_owner(user) or user.has_perm("catalog.can_unpublish_product")

    def can_delete(self, user):
        """Проверяет, может ли пользователь удалить продукт"""
        return self.is_owner(user) or user.has_perm("catalog.delete_product")
