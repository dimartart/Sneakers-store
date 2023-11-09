from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    brand = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, verbose_name="URL", db_index=True, blank=True, unique=True)

    def __str__(self):
        return self.brand

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    model_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, verbose_name="URL", db_index=True, blank=True, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=None)
    photo = models.ImageField(upload_to="photo/%Y/%m/%d/")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.model_name

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})


class Storage(models.Model):
    size = models.IntegerField()
    amount = models.IntegerField()
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.product) + " " + str(self.size) + " size"

    class Meta:
        verbose_name_plural = "Storage"


class Order(models.Model):
    items_amount = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    date_of_payment = models.DateTimeField(blank=True, null=True)
    client_username = models.CharField(max_length=255)
    client_mail = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Products in orders"
