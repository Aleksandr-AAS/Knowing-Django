from django import forms
from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    """
    Форма для создания и редактирования блоговой записи
    """

    class Meta:
        model = BlogPost
        fields = ["title", "content", "preview", "is_published"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 10}),
        }
        labels = {
            "title": "Заголовок",
            "content": "Содержимое",
            "preview": "Превью (изображение)",
            "is_published": "Опубликовать",
        }
