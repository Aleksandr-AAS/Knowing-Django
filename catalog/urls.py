from django.urls import path
from . import views

urlpatterns = [
    # Главная страница (CBV)
    path("", views.HomeView.as_view(), name="home"),
    # Страница контактов (CBV)
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
    # Детальная страница товара (CBV)
    path("product/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
]
