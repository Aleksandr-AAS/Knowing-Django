from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """
    Форма для создания и редактирования продукта
    """

    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price", "is_published"]
        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 5, "placeholder": "Описание товара..."}
            ),
            "name": forms.TextInput(attrs={"placeholder": "Введите название товара"}),
            "price": forms.NumberInput(
                attrs={"step": "0.01", "placeholder": "0.00", "min": "0"}
            ),
            "is_published": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
        }
        labels = {
            "name": "Название товара",
            "description": "Описание",
            "image": "Изображение",
            "category": "Категория",
            "price": "Цена (₽)",
            "is_published": "Опубликовать товар",
        }

    # Список запрещенных слов
    FORBIDDEN_WORDS = [
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    ]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name:
            name_lower = name.lower()
            found_words = [w for w in self.FORBIDDEN_WORDS if w in name_lower]
            if found_words:
                raise forms.ValidationError(
                    f'Название содержит запрещенные слова: {", ".join(found_words)}'
                )
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if description:
            desc_lower = description.lower()
            found_words = [w for w in self.FORBIDDEN_WORDS if w in desc_lower]
            if found_words:
                raise forms.ValidationError(
                    f'Описание содержит запрещенные слова: {", ".join(found_words)}'
                )
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price
