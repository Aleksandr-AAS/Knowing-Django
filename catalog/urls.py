from django.urls import path
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.conf import settings
from . import views

app_name = "catalog"

# Получаем время кеширования из настроек
PRODUCT_DETAIL_TIMEOUT = getattr(settings, "CACHE_TIMEOUTS", {}).get(
    "product_detail", 60 * 15
)
CATEGORY_PAGE_TIMEOUT = getattr(settings, "CACHE_TIMEOUTS", {}).get(
    "category_page", 60 * 10
)

urlpatterns = [
    # Публичные страницы
    path("", views.HomeView.as_view(), name="home"),
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
    # Страница категории с кешированием
    path(
        "category/<int:pk>/",
        cache_page(CATEGORY_PAGE_TIMEOUT)(views.CategoryProductsView.as_view()),
        name="category_products",
    ),
    # Детальная страница товара с кешированием
    path(
        "product/<int:pk>/",
        vary_on_headers("Cookie")(
            cache_page(PRODUCT_DETAIL_TIMEOUT)(views.ProductDetailView.as_view())
        ),
        name="product_detail",
    ),
    # Управление продуктами
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path("products/create/", views.ProductCreateView.as_view(), name="product_create"),
    path(
        "products/<int:pk>/update/",
        views.ProductUpdateView.as_view(),
        name="product_update",
    ),
    path(
        "products/<int:pk>/delete/",
        views.ProductDeleteView.as_view(),
        name="product_delete",
    ),
    path(
        "products/<int:pk>/toggle-publish/",
        views.ProductTogglePublishView.as_view(),
        name="product_toggle_publish",
    ),
]
