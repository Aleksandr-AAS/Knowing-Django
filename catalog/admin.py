# from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category")
    list_filter = ("category",)
    search_fields = ("name", "description")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
