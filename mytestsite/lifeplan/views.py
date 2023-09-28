from django.http import HttpResponse
from django.shortcuts import render

from .models import *

menu = [{'title': "Home", 'url_name': 'base'},
        {'title': "Contact", 'url_name': 'contact'},
        {'title': "Help", 'url_name': 'help'}
]

# Create your views here.
def base(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'products': products,
        'menu': menu,
        'categories': categories
    }
    return render(request, 'lifeplan/base.html', context=context)


def contact(request):
    return render(request, 'lifeplan/contact.html')


def help(request):
    return render(request, 'lifeplan/help.html')

def show_product(request, product_id):
    return HttpResponse(f"sneakers with id{product_id}")