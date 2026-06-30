from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate


class CustomUserCreationForm(UserCreationForm):
    """
    Форма для регистрации нового пользователя
    """

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "example@mail.com"}
        ),
    )

    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите имя пользователя"}
        ),
    )

    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Иван"}),
    )

    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Иванов"}
        ),
    )

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        ),
    )

    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Повторите пароль"}
        ),
    )

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

    def clean_email(self):
        """Проверка уникальности email"""
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean_username(self):
        """Проверка уникальности username"""
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким именем уже существует.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    """
    Форма для редактирования профиля пользователя
    """

    class Meta:
        model = CustomUser
        fields = (
            "avatar",
            "first_name",
            "last_name",
            "phone",
            "country",
            "bio",
            "birth_date",
        )
        widgets = {
            "avatar": forms.FileInput(
                attrs={"class": "form-control", "accept": "image/*"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Иван"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Иванов"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "+7 (999) 123-45-67"}
            ),
            "country": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Россия"}
            ),
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Расскажите о себе...",
                }
            ),
            "birth_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "placeholder": "1990-01-01",
                }
            ),
        }

    def clean_phone(self):
        """Валидация номера телефона"""
        phone = self.cleaned_data.get("phone")
        if phone and len(phone) < 10:
            raise ValidationError("Введите корректный номер телефона.")
        return phone


class CustomAuthenticationForm(AuthenticationForm):
    """
    Кастомная форма для авторизации по email
    """

    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "example@mail.com",
                "autofocus": True,
            }
        ),
    )

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        ),
    )

    error_messages = {
        "invalid_login": (
            "Неверный email или пароль. Пожалуйста, проверьте введенные данные."
        ),
        "inactive": "Этот аккаунт не активирован. Обратитесь к администратору.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Переименовываем поле username в email для отображения
        self.fields["username"].label = "Email"

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            # Аутентификация через кастомный бэкенд
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
