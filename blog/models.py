from django.db import models
from django.urls import reverse


class BlogPost(models.Model):
    """
    Модель блоговой записи
    """

    title = models.CharField(max_length=200, verbose_name="Заголовок")

    content = models.TextField(verbose_name="Содержимое")

    preview = models.ImageField(
        upload_to="blog_previews/",
        verbose_name="Превью (изображение)",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    is_published = models.BooleanField(default=False, verbose_name="Признак публикации")

    views_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество просмотров"
    )

    class Meta:
        verbose_name = "блоговая запись"
        verbose_name_plural = "блоговые записи"
        ordering = ["-created_at"]  # сортировка по дате создания (новые сверху)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Возвращает URL для детальной страницы записи
        Используется в CBV для редиректа после создания/обновления
        """
        return reverse("blog:post_detail", args=[self.pk])
