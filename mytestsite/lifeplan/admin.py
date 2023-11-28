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


class OrderAdmin(admin.ModelAdmin):
    list_display = ("client_username", "items_amount", "total_price")


class ProductInOrderAdmin(admin.ModelAdmin):
    list_display = ("order", "order_client_username", "product", "size_of_product")

    def order_client_username(self, obj):
        return obj.order.client_username

    order_client_username.short_description = 'Client Username'


admin.site.register(ProductInOrder, ProductInOrderAdmin)
admin.site.register(Storage, StorageAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)

