from django.contrib import admin

# Register your models here.
from .models import *


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("model_name",)}
    list_display =("id", "model_name", "photo", "category")
    list_display_links =("id", "model_name")


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("brand",)}

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order)
admin.site.register(Supply)

