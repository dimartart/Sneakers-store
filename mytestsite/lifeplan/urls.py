from django.urls import path

from .views import *

urlpatterns = [
    path('', base, name='base'),
    path('contact/', contact, name='contact'),
    path('help/', contact, name='help')
]