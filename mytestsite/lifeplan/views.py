from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import RegisterUserForm
from .models import *
from .utils import DataMixin
menu = [{'title': "Home", 'url_name': 'base'},
        {'title': "Contact", 'url_name': 'contact'},
        {'title': "Help", 'url_name': 'help'}
]


# Create your views here.
class MainPage(DataMixin, ListView):
    model = Product
    template_name = 'lifeplan/base.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title="Main page")
        return dict(list(context.items()) + list(mixin_context.items()))


def contact(request):
    context = {
        'menu': menu,
        'title': 'Contacts'
    }
    return render(request, 'lifeplan/contact.html', context=context)


def help(request):
    context = {
        'menu': menu,
        'title': 'Help'
    }
    return render(request, 'lifeplan/help.html', context=context)


def cart(request):
    context = {
        'menu': menu,
        'title': 'Cart'
    }
    return render(request, 'lifeplan/cart.html', context=context)


class ShowProduct(DataMixin, DetailView):
    model = Product
    template_name = "lifeplan/product.html"
    slug_url_kwarg = "product_slug"
    context_object_name = "product"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_id = context["product"].category_id
        mixin_context = self.get_user_context(title=context["product"], selected_category=cat_id)
        return dict(list(context.items()) + list(mixin_context.items()))


class SneakersCategory(DataMixin, ListView):
    model = Category
    template_name = 'lifeplan/base.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        self.category_title = Category.objects.get(slug=category_slug)
        return Product.objects.filter(category__slug=category_slug)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_id = self.category_title.pk
        mixin_context = self.get_user_context(title=self.category_title.brand, selected_category=cat_id)
        return dict(list(context.items()) + list(mixin_context.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'lifeplan/registration.html'
    success_url = reverse_lazy('base')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title="Registration")
        return dict(list(context.items()) + list(mixin_context.items()))


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'lifeplan/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title="Log In")
        return dict(list(context.items()) + list(mixin_context.items()))
#
# def show_category(request, category_slug):
#     products = Product.objects.filter(category__slug=category_slug)
#     category_title = Category.objects.get(slug=category_slug)
#     context = {
#         'products': products,
#         'menu': menu,
#         'selected_category': category_title.pk,
#         'title': category_title
#     }
#     return render(request, 'lifeplan/base.html', context=context)


# def base(request):
#     products = Product.objects.all()
#     context = {
#         'products': products,
#         'menu': menu,
#         'selected_category': 0,
#         'title': 'Sneakers shop'
#     }
#     return render(request, 'lifeplan/base.html', context=context)

# def show_product(request, product_slug):
#     product = get_object_or_404(Product, slug=product_slug)
#
#     context = {
#         'product': product,
#         'menu': menu,
#         'selected_category': product.category_id,
#         'title': product.model_name
#     }
#
#     return render(request, 'lifeplan/product.html', context=context)