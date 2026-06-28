from django.test import TestCase
from django.contrib.auth import get_user_model
from catalog.models import Category, Product

User = get_user_model()


class CategoryModelTest(TestCase):
    """Тесты для модели Category"""

    def test_category_creation(self):
        category = Category.objects.create(
            name="Тестовая категория", description="Описание категории"
        )
        self.assertEqual(category.name, "Тестовая категория")
        self.assertEqual(str(category), "Тестовая категория")


class ProductModelTest(TestCase):
    """Тесты для модели Product"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.ru", password="testpass123"
        )
        self.category = Category.objects.create(
            name="Электроника", description="Всё для дома"
        )

    def test_product_creation(self):
        product = Product.objects.create(
            name="Смартфон",
            description="Новый смартфон",
            category=self.category,
            price=50000,
            owner=self.user,
            is_published=True,
        )
        self.assertEqual(product.name, "Смартфон")
        self.assertEqual(product.price, 50000)
        self.assertEqual(str(product), "Смартфон")

    def test_product_is_owner(self):
        product = Product.objects.create(
            name="Ноутбук", category=self.category, price=80000, owner=self.user
        )
        self.assertTrue(product.is_owner(self.user))
