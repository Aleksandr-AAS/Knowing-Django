from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Кастомизация админ-панели для модели пользователя
    """

    # Поля, отображаемые в списке пользователей
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "phone",
        "country",
        "is_active",
        "date_joined",
    )

    # Поля для поиска
    search_fields = ("email", "username", "first_name", "last_name", "phone")

    # Фильтры
    list_filter = ("is_active", "is_staff", "is_superuser", "country", "date_joined")

    # Поля для редактирования
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        (
            _("Личная информация"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "avatar",
                    "phone",
                    "country",
                    "bio",
                    "birth_date",
                )
            },
        ),
        (
            _("Права доступа"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Важные даты"), {"fields": ("last_login", "date_joined", "last_activity")}),
    )

    # Поля для добавления нового пользователя
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )

    # Поля, доступные только для чтения
    readonly_fields = ("date_joined", "last_login", "last_activity")

    # Сортировка по умолчанию
    ordering = ("-date_joined",)
