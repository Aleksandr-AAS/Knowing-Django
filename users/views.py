from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .utils import send_welcome_email
from .forms import CustomAuthenticationForm
from django.conf import settings


class RegisterView(CreateView):
    """
    Контроллер для регистрации пользователя
    """

    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form):
        """Автоматический вход после регистрации и отправка приветственного письма"""
        response = super().form_valid(form)
        user = form.save()

        # Устанавливаем бэкенд для пользователя
        user.backend = settings.AUTHENTICATION_BACKENDS[0]

        # Автоматический вход пользователя после регистрации
        login(self.request, user)

        # Отправляем приветственное письмо
        try:
            send_welcome_email(user)
            messages.success(
                self.request,
                "Регистрация прошла успешно! Приветственное письмо отправлено на ваш email.",
            )
        except Exception as e:
            messages.warning(
                self.request,
                "Регистрация прошла успешно, но не удалось отправить приветственное письмо.",
            )
            print(f"Ошибка отправки письма: {e}")

        return response

    def form_invalid(self, form):
        messages.error(self.request, "Исправьте ошибки в форме.")
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    """
    Контроллер для входа пользователя по email
    """

    template_name = "users/login.html"
    authentication_form = CustomAuthenticationForm  # ← кастомная форма для email
    redirect_authenticated_user = True

    def get_success_url(self):
        """Перенаправление после успешного входа"""
        return reverse_lazy("catalog:home")

    def form_valid(self, form):
        """При успешном входе показываем сообщение"""
        user = form.get_user()
        messages.success(
            self.request, f"С возвращением, {user.get_full_name() or user.username}!"
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        """При ошибке входа показываем сообщение"""
        messages.error(self.request, "Неверный email или пароль. Попробуйте еще раз.")
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    """
    Контроллер для выхода пользователя
    """

    next_page = reverse_lazy("catalog:home")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Вы вышли из системы.")
        return super().dispatch(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, DetailView):
    """
    Контроллер для просмотра профиля пользователя
    """

    model = CustomUser
    template_name = "users/profile.html"
    context_object_name = "profile_user"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_owner"] = True
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер для редактирования профиля пользователя
    """

    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "users/profile_edit.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("users:profile")

    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно обновлен!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Исправьте ошибки в форме.")
        return super().form_invalid(form)
