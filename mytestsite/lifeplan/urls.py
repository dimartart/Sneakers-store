from django.urls import path

from .views import *

urlpatterns = [
    path('', base, name='base'),
    path('contact/', contact, name='contact'),
    path('help/', help, name='help'),
    path('login/', contact, name='login'),
    path('registration/', contact, name='registration'),
    path('sneakers/<int:product_id>', show_product, name='product')
]