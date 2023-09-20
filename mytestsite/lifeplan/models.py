from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    brand = models.CharField(max_length=255)

    def __str__(self):
        return self.brand


class Product(models.Model):
    model_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photo/%Y/%m/%d/")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.model_name


class Supply(models.Model):
    size = models.IntegerField(max_length=3)
    price = models.DecimalField(max_digits=10, decimal_places=2 )
    amount = models.IntegerField(max_length=4)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    def __str__(self):
        return self.product


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
