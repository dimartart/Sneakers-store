from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *
from . import views

urlpatterns = [
    # path('', cache_page(60)(MainPage.as_view()), name='base'),
    path('', MainPage.as_view(), name='base'),
    path('contact/', contact, name='contact'),
    path('help/', help, name='help'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('sneakers/<slug:product_slug>', ShowProduct.as_view(), name='product'),
    path('category/<slug:category_slug>', SneakersCategory.as_view(), name='category'),
    path('cart/', cart, name='cart'),
    path('user_info/', user, name='user'),
    path('handle_ajax_request', views.handle_ajax_request, name='handle_ajax_request'),
    path('remove_from_cart', views.remove_from_cart, name='remove_from_cart')
]
