from django.core.cache import cache
from django.conf import settings
from .models import Product, Category


def get_products_by_category(category_id, published_only=True):
    """
    Сервисная функция: возвращает список продуктов в указанной категории

    Args:
        category_id (int): ID категории
        published_only (bool): Только опубликованные товары

    Returns:
        QuerySet: Список продуктов в категории
    """
    cache_key = (
        f'category_products_{category_id}_{"published" if published_only else "all"}'
    )
    timeout = getattr(settings, "CACHE_TIMEOUTS", {}).get("category_page", 60 * 10)

    # Пытаемся получить из кеша
    products = cache.get(cache_key)

    if products is None:
        # Формируем запрос
        queryset = Product.objects.filter(category_id=category_id)

        if published_only:
            queryset = queryset.filter(is_published=True)

        products = queryset.select_related("category", "owner").order_by("-created_at")

        # Сохраняем в кеш (только для списка, не для QuerySet)
        cache.set(cache_key, list(products), timeout)

    return products


def get_category_by_id(category_id):
    """
    Сервисная функция: возвращает категорию по ID с кешированием
    """
    cache_key = f"category_{category_id}"
    timeout = getattr(settings, "CACHE_TIMEOUTS", {}).get("category_page", 60 * 10)

    category = cache.get(cache_key)

    if category is None:
        try:
            category = Category.objects.get(id=category_id)
            cache.set(cache_key, category, timeout)
        except Category.DoesNotExist:
            return None

    return category


def get_all_categories():
    """
    Сервисная функция: возвращает все категории для меню
    """
    cache_key = "all_categories_list"
    timeout = getattr(settings, "CACHE_TIMEOUTS", {}).get("category_page", 60 * 10)

    categories = cache.get(cache_key)

    if categories is None:
        categories = list(Category.objects.all())
        cache.set(cache_key, categories, timeout)

    return categories


def clear_category_cache(category_id=None):
    """
    Сервисная функция: очищает кеш категорий
    """
    # Очищаем кеш конкретной категории
    if category_id:
        cache.delete(f"category_products_{category_id}_published")
        cache.delete(f"category_products_{category_id}_all")
        cache.delete(f"category_{category_id}")

    # Очищаем общий кеш
    cache.delete("all_categories_list")
