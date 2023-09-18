from django.http import HttpResponse
from django.shortcuts import render

from .models import *

menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]

# Create your views here.
def base(request):
    return render(request, 'lifeplan/base.html')

def contact(request):
    return render(request, 'lifeplan/contact.html')
