from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy, reverse
from .models import BlogPost
from .forms import BlogPostForm


class BlogPostListView(ListView):
    """
    Контроллер для отображения списка блоговых записей
    """

    model = BlogPost
    template_name = "blog/blogpost_list.html"
    context_object_name = "posts"
    paginate_by = 6  # пагинация по 6 записей на странице

    def get_queryset(self):
        """
        Фильтрация опубликованных статей:
        Выводим в список только те статьи, у которых is_published = True
        """
        return BlogPost.objects.filter(is_published=True).order_by("-created_at")


class BlogPostDetailView(DetailView):
    """
    Контроллер для детальной страницы блоговой записи
    """

    model = BlogPost
    template_name = "blog/blogpost_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        """
        Увеличение счетчика просмотров:
        При открытии отдельной статьи увеличиваем счетчик просмотров
        """
        # Получаем объект статьи
        obj = super().get_object(queryset)

        # Увеличиваем счетчик просмотров на 1
        obj.views_count += 1

        # Сохраняем только поле views_count (оптимизация)
        obj.save(update_fields=["views_count"])

        return obj


class BlogPostCreateView(CreateView):
    """
    Контроллер для создания новой блоговой записи
    """

    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/blogpost_form.html"
    success_url = reverse_lazy("blog:post_list")

    def form_valid(self, form):
        """
        При создании записи можно добавить дополнительную логику
        """
        return super().form_valid(form)


class BlogPostUpdateView(UpdateView):
    """
    Контроллер для редактирования блоговой записи
    """

    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/blogpost_form.html"

    def get_success_url(self):
        """
        Перенаправление после редактирования:
        После успешного редактирования перенаправляем на просмотр этой статьи
        """
        # reverse возвращает URL для детальной страницы текущей статьи
        return reverse("blog:post_detail", kwargs={"pk": self.object.pk})


class BlogPostDeleteView(DeleteView):
    """
    Контроллер для удаления блоговой записи
    """

    model = BlogPost
    template_name = "blog/blogpost_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")
