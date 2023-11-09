from django.contrib import admin

# Register your models here.
from .models import *


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("model_name",)}
    list_display = ("id", "model_name", "price", "photo", "category")
    list_display_links = ("id", "model_name")
    search_fields = ("model_name",)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("brand",)}


class StorageAdmin(admin.ModelAdmin):
    list_display = ("size", "amount", "product")


class ProductInOrderAdmin(admin.ModelAdmin):
    list_display = ("order", "product")


admin.site.register(ProductInOrder, ProductInOrderAdmin)
admin.site.register(Storage, StorageAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order)

