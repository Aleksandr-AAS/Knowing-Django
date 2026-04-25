from django.core.cache import cache
from django.conf import settings


def clear_all_cache():
    """
    Очищает весь кеш
    """
    cache.clear()
    print("✅ Весь кеш очищен")


def clear_product_cache(product_id=None):
    """
    Очищает кеш связанный с продуктами
    """
    # Очищаем кеш главной страницы
    cache.delete(
        getattr(settings, "CACHE_KEYS", {}).get("home_products", "home_products_list")
    )

    # Очищаем кеш конкретного продукта
    if product_id:
        cache.delete(f"catalog:product_detail_{product_id}")

    # Очищаем кеш для модератора
    cache.delete("all_products_for_moderator")

    print(
        "✅ Кеш продуктов очищен" + (f" для товара {product_id}" if product_id else "")
    )


def get_cache_stats():
    """
    Получает статистику по кешу (для отладки)
    """
    stats = {
        "CACHE_ENABLED": getattr(settings, "CACHE_ENABLED", True),
        "CACHE_BACKEND": settings.CACHES["default"]["BACKEND"],
        "CACHE_TIMEOUTS": getattr(settings, "CACHE_TIMEOUTS", {}),
        "HOME_CACHE_KEY": getattr(settings, "CACHE_KEYS", {}).get(
            "home_products", "home_products_list"
        ),
    }
    return stats
