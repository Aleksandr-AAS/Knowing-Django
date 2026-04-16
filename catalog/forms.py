from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """
    Форма для создания и редактирования продукта с валидацией и стилизацией
    """

    # Список запрещенных слов (в нижнем регистре)
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

    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]
        labels = {
            "name": "Название товара",
            "description": "Описание",
            "image": "Изображение",
            "category": "Категория",
            "price": "Цена (₽)",
        }
        help_texts = {
            "image": "Загрузите изображение товара (опционально)",
            "price": "Цена в рублях. Может быть 0 для бесплатных товаров",
        }

    def __init__(self, *args, **kwargs):
        """
        ✅ Стилизация формы через метод __init__
        Добавляем CSS-классы, атрибуты и виджеты для всех полей
        """
        super().__init__(*args, **kwargs)

        # Общие стили для всех полей
        for field_name, field in self.fields.items():
            # Добавляем CSS класс form-control для всех полей
            if field.widget.attrs.get("class"):
                field.widget.attrs["class"] += " form-control"
            else:
                field.widget.attrs["class"] = "form-control"

            # Добавляем атрибут placeholder для текстовых полей
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs["placeholder"] = f"Введите {field.label.lower()}"
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs["placeholder"] = f"Введите {field.label.lower()}"
                field.widget.attrs["rows"] = 6
            elif isinstance(field.widget, forms.NumberInput):
                field.widget.attrs["placeholder"] = "0.00"
                field.widget.attrs["step"] = "0.01"
                field.widget.attrs["min"] = "0"
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] += " form-select"
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs["class"] += " form-file"
                field.widget.attrs["accept"] = "image/*"

        # Индивидуальные настройки для конкретных полей
        self.fields["name"].widget.attrs.update(
            {
                "autofocus": "autofocus",
                "placeholder": "Введите название товара (например: Смартфон Xiaomi)",
            }
        )

        self.fields["description"].widget.attrs.update(
            {
                "placeholder": "Подробное описание товара...",
                "rows": 8,
            }
        )

        self.fields["price"].widget.attrs.update(
            {
                "placeholder": "0.00",
                "step": "0.01",
                "min": "0",
            }
        )

        self.fields["category"].widget.attrs.update(
            {
                "class": "form-select",
            }
        )

        self.fields["image"].widget.attrs.update(
            {
                "accept": "image/jpeg,image/png,image/gif,image/webp",
                "class": "form-file",
            }
        )

    def _check_forbidden_words(self, value, field_name):
        """
        Проверяет наличие запрещенных слов в значении поля
        Возвращает список найденных запрещенных слов
        """
        if not value:
            return []

        value_lower = value.lower()
        found_words = []

        for word in self.FORBIDDEN_WORDS:
            if word in value_lower:
                found_words.append(word)

        return found_words

    def clean_name(self):
        """
        Валидация названия продукта
        """
        name = self.cleaned_data.get("name")

        if name:
            found_words = self._check_forbidden_words(name, "name")
            if found_words:
                raise forms.ValidationError(
                    f'⚠️ Название содержит запрещенные слова: {", ".join(found_words)}. '
                    f"Пожалуйста, удалите их."
                )

        return name

    def clean_description(self):
        """
        Валидация описания продукта
        """
        description = self.cleaned_data.get("description")

        if description:
            found_words = self._check_forbidden_words(description, "description")
            if found_words:
                raise forms.ValidationError(
                    f'⚠️ Описание содержит запрещенные слова: {", ".join(found_words)}. '
                    f"Пожалуйста, удалите их."
                )

        return description

    def clean_price(self):
        """
        Кастомная валидация цены продукта
        Проверяет, что цена не может быть отрицательной
        """
        price = self.cleaned_data.get("price")

        if price is not None and price < 0:
            raise forms.ValidationError(
                "❌ Цена товара не может быть отрицательной. "
                "Пожалуйста, введите корректную цену (0 или больше)."
            )

        if price is not None and price > 1000000:
            raise forms.ValidationError(
                "⚠️ Цена не может превышать 1 000 000 ₽. "
                "Если товар стоит дороже, пожалуйста, свяжитесь с администратором."
            )

        return price
