from django.urls import path
from . import views

app_name = "catalog"
urlpatterns = [
    # Главная страница (CBV)
    path("", views.HomeView.as_view(), name="home"),
    # Страница контактов (CBV)
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
    # Детальная страница товара (CBV)
    path("product/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
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
]
