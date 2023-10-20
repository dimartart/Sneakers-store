from django.urls import path

from .views import *

urlpatterns = [
    path('', MainPage.as_view(), name='base'),
    path('contact/', contact, name='contact'),
    path('help/', help, name='help'),
    path('login/', LoginUser.as_view(), name='login'),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('sneakers/<slug:product_slug>', ShowProduct.as_view(), name='product'),
    path('category/<slug:category_slug>', SneakersCategory.as_view(), name='category'),
    path('cart/', cart, name='cart')
]