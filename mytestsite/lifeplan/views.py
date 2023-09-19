from django.http import HttpResponse
from django.shortcuts import render

from .models import *

menu = [{'title': "Contact", 'url_name': 'contact'},
        {'title': "Help page", 'url_name': 'help'}
]

# Create your views here.
def base(request):
    return render(request, 'lifeplan/base.html')

def contact(request):
    return render(request, 'lifeplan/contact.html')

def help(request):
    return render(request, 'lifeplan/help.html')
