from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class EmailAuthBackend(ModelBackend):
    """
    Бэкенд для авторизации пользователя по email или username
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Аутентификация пользователя по email или username
        """
        if username is None:
            return None

        try:
            # Пытаемся найти пользователя по email или username
            user = User.objects.get(Q(email=username) | Q(username=username))
        except User.DoesNotExist:
            # Запускаем стандартный процесс аутентификации
            return super().authenticate(request, username=username, password=password, **kwargs)

        # Проверяем пароль
        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None