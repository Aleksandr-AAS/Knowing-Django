from django.urls import path
from . import views

app_name = "blog"  # пространство имен для ссылок

urlpatterns = [
    # CRUD маршруты для блога
    path("", views.BlogPostListView.as_view(), name="post_list"),  # Read (список)
    path(
        "<int:pk>/", views.BlogPostDetailView.as_view(), name="post_detail"
    ),  # Read (детально)
    path("create/", views.BlogPostCreateView.as_view(), name="post_create"),  # Create
    path(
        "<int:pk>/update/", views.BlogPostUpdateView.as_view(), name="post_update"
    ),  # Update
    path(
        "<int:pk>/delete/", views.BlogPostDeleteView.as_view(), name="post_delete"
    ),  # Delete
]
