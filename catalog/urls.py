from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    # Публичные страницы
    path("", views.HomeView.as_view(), name="home"),
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
    path("product/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
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
    # Дополнительный URL для переключения публикации
    path(
        "products/<int:pk>/toggle-publish/",
        views.ProductTogglePublishView.as_view(),
        name="product_toggle_publish",
    ),
]
