from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_welcome_email(user):
    """
    Отправляет приветственное письмо пользователю после регистрации
    """
    subject = "Добро пожаловать в наш каталог!"

    # HTML версия письма
    html_message = render_to_string(
        "users/emails/welcome_email.html",
        {
            "user": user,
            "site_url": "http://127.0.0.1:8000",
            "profile_url": "http://127.0.0.1:8000/users/profile/",
        },
    )

    # Текстовая версия письма (для почтовых клиентов без HTML)
    plain_message = strip_tags(html_message)

    # Отправляем письмо
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )
