from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from catalog.models import Category, Product

User = get_user_model()


class CatalogViewsTest(TestCase):
    """Тесты для представлений каталога"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.ru", password="testpass123"
        )
        self.category = Category.objects.create(
            name="Книги", description="Книги разных жанров"
        )
        self.product = Product.objects.create(
            name="Война и мир",
            category=self.category,
            price=1500,
            owner=self.user,
            is_published=True,
        )

    def test_homepage_status(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_catalog_page_status(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_product_detail_page(self):
        response = self.client.get(
            reverse("catalog:product_detail", args=[self.product.pk])
        )
        self.assertEqual(response.status_code, 200)
