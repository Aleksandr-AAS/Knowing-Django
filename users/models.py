from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя с email в качестве поля для авторизации
    """

    # Дополнительные поля
    email = models.EmailField(
        _("email address"),
        unique=True,  # email должен быть уникальным
        help_text="Введите действующий email адрес",
    )

    avatar = models.ImageField(
        _("аватар"),
        upload_to="avatars/",
        blank=True,
        null=True,
        help_text="Загрузите изображение для аватара (опционально)",
    )

    phone = models.CharField(
        _("номер телефона"),
        max_length=20,
        blank=True,
        null=True,
        help_text="Введите номер телефона в международном формате",
    )

    country = models.CharField(
        _("страна"),
        max_length=100,
        blank=True,
        null=True,
        help_text="Укажите вашу страну проживания",
    )

    # Дополнительные поля для информации о пользователе
    bio = models.TextField(
        _("о себе"),
        max_length=500,
        blank=True,
        null=True,
        help_text="Краткая информация о вас",
    )

    birth_date = models.DateField(
        _("дата рождения"), blank=True, null=True, help_text="ДД.ММ.ГГГГ"
    )

    # Поле для отслеживания активности
    last_activity = models.DateTimeField(_("последняя активность"), auto_now=True)

    # Настройка для авторизации через email
    USERNAME_FIELD = "email"  # Поле для авторизации
    REQUIRED_FIELDS = ["username"]  # Обязательные поля при создании суперпользователя

    class Meta:
        verbose_name = _("пользователь")
        verbose_name_plural = _("пользователи")
        ordering = ["-date_joined"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Возвращает полное имя пользователя"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    def get_short_name(self):
        """Возвращает короткое имя пользователя"""
        return self.first_name or self.username
