from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product
import os


class Command(BaseCommand):
    help = "Добавляет тестовые продукты в базу данных, очищая существующие"

    def add_arguments(self, parser):
        # Опциональный аргумент для выбора метода загрузки
        parser.add_argument(
            "--method",
            type=str,
            choices=["orm", "fixture"],
            default="orm",
            help="Метод загрузки: orm (через Django ORM) или fixture (из фикстур)",
        )

        parser.add_argument(
            "--fixture-file",
            type=str,
            default="catalog/fixtures/initial_data.json",
            help="Путь к файлу фикстуры (если method=fixture)",
        )

    def handle(self, *args, **options):
        method = options["method"]
        fixture_file = options["fixture_file"]

        self.stdout.write(self.style.WARNING("Очищаем существующие данные..."))
        self.clear_data()

        self.stdout.write(
            self.style.WARNING(f"Загружаем тестовые данные методом: {method}...")
        )

        if method == "orm":
            self.load_data_orm()
        else:  # fixture
            self.load_data_fixture(fixture_file)

        self.stdout.write(self.style.SUCCESS("Тестовые продукты успешно добавлены!"))

        self.show_stats()

    def clear_data(self):
        """Очищает все данные из моделей в правильном порядке"""

        products_count = Product.objects.count()
        Product.objects.all().delete()
        self.stdout.write(f"  - Удалено продуктов: {products_count}")

        categories_count = Category.objects.count()
        Category.objects.all().delete()
        self.stdout.write(f"  - Удалено категорий: {categories_count}")

    def load_data_orm(self):
        """Загружает тестовые данные через ORM"""
        self.stdout.write(self.style.WARNING("  Создаем категории..."))

        categories = [
            Category(name="Смартфоны"),
            Category(name="Ноутбуки"),
            Category(name="Планшеты"),
            Category(name="Наушники"),
            Category(name="Аксессуары"),
        ]
        Category.objects.bulk_create(categories)
        self.stdout.write(f"    + Создано категорий: {len(categories)}")

        smartphones = Category.objects.get(name="Смартфоны")
        laptops = Category.objects.get(name="Ноутбуки")
        tablets = Category.objects.get(name="Планшеты")
        headphones = Category.objects.get(name="Наушники")
        accessories = Category.objects.get(name="Аксессуары")

        self.stdout.write(self.style.WARNING("  Создаем продукты..."))

        # Создаем продукты
        products = [
            # Смартфоны
            Product(
                name="iPhone 15 Pro",
                price=1199.99,
                category=smartphones,
                description="Флагман Apple с титановым корпусом и чипом A17 Pro",
            ),
            Product(
                name="Samsung Galaxy S24 Ultra",
                price=1299.99,
                category=smartphones,
                description="Флагман Samsung с AI-функциями и S Pen",
            ),
            Product(
                name="Google Pixel 8 Pro",
                price=999.99,
                category=smartphones,
                description="Камера с AI-обработкой и чистый Android",
            ),
            Product(
                name="Xiaomi 14 Ultra",
                price=899.99,
                category=smartphones,
                description="Камера Leica и мощный процессор",
            ),
            # Ноутбуки
            Product(
                name="MacBook Pro 16",
                price=2499.99,
                category=laptops,
                description="Профессиональный ноутбук с чипом M3 Max",
            ),
            Product(
                name="Dell XPS 15",
                price=1899.99,
                category=laptops,
                description="Премиальный ультрабук с OLED-экраном",
            ),
            Product(
                name="ASUS ROG Strix",
                price=1799.99,
                category=laptops,
                description="Игровой ноутбук с RTX 4080",
            ),
            Product(
                name="Lenovo ThinkPad X1",
                price=1599.99,
                category=laptops,
                description="Бизнес-ноутбук с отличной клавиатурой",
            ),
            # Планшеты
            Product(
                name="iPad Pro 12.9",
                price=1299.99,
                category=tablets,
                description="Планшет с чипом M2 и XDR дисплеем",
            ),
            Product(
                name="Samsung Tab S9 Ultra",
                price=1199.99,
                category=tablets,
                description="Флагманский планшет с AMOLED-экраном",
            ),
            # Наушники
            Product(
                name="AirPods Max",
                price=549.99,
                category=headphones,
                description="Премиальные наушники от Apple",
            ),
            Product(
                name="Sony WH-1000XM5",
                price=399.99,
                category=headphones,
                description="Лучшее шумоподавление на рынке",
            ),
            Product(
                name="Bose QuietComfort",
                price=349.99,
                category=headphones,
                description="Комфортные наушники для путешествий",
            ),
            # Аксессуары
            Product(
                name="Apple Watch Series 9",
                price=429.99,
                category=accessories,
                description="Умные часы с новым жестом двойного касания",
            ),
            Product(
                name="Magic Mouse",
                price=79.99,
                category=accessories,
                description="Беспроводная мышь от Apple",
            ),
            Product(
                name="Logitech MX Master 3S",
                price=99.99,
                category=accessories,
                description="Эргономичная мышь для продуктивности",
            ),
        ]

        Product.objects.bulk_create(products)
        self.stdout.write(f"    + Создано продуктов: {len(products)}")

    def load_data_fixture(self, fixture_file):
        """Загружает данные из фикстуры"""
        try:
            # Проверяем существование файла
            if not os.path.exists(fixture_file):
                self.stdout.write(
                    self.style.ERROR(f" Файл фикстуры {fixture_file} не найден!")
                )
                self.stdout.write(self.style.WARNING("Пытаемся загрузить через ORM..."))
                self.load_data_orm()
                return

            # Загружаем фикстуру
            call_command("loaddata", fixture_file)
            self.stdout.write(
                self.style.SUCCESS(f"   Фикстура {fixture_file} загружена")
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f" Ошибка загрузки фикстуры: {e}"))
            self.stdout.write(self.style.WARNING("Пытаемся загрузить через ORM..."))
            self.load_data_orm()

    def show_stats(self):
        """Показывает статистику после загрузки"""
        self.stdout.write(self.style.SUCCESS("\n Статистика:"))
        self.stdout.write(f"  Категорий: {Category.objects.count()}")
        self.stdout.write(f"  Продуктов: {Product.objects.count()}")

        # Показываем по категориям
        self.stdout.write(self.style.WARNING("\n  По категориям:"))
        for category in Category.objects.all():
            count = Product.objects.filter(category=category).count()
            self.stdout.write(f"    • {category.name}: {count} продуктов")
