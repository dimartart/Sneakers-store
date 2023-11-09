from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from .models import *
from .utils import DataMixin
from django.http import JsonResponse

menu = [
    {'title': "Home", 'url_name': 'base'},
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


class ShowProduct(DataMixin, DetailView):
    model = Product
    template_name = "lifeplan/product.html"
    slug_url_kwarg = "product_slug"
    context_object_name = "product"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_id = context["product"].category_id
        mixin_context = self.get_user_context(title=context["product"], selected_category=cat_id)

        product = kwargs.get('object')
        storage_info = Storage.objects.filter(product=product)
        context["storage_info"] = storage_info
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

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('base')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'lifeplan/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title="Log In")
        return dict(list(context.items()) + list(mixin_context.items()))

    def get_success_url(self):
        return reverse_lazy('base')


def logout_user(request):
    logout(request)
    return redirect('login')


def user(request):
    context = {
        'menu': menu,
        'title': 'User'
    }
    return render(request, 'lifeplan/user.html', context=context)


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


def handle_ajax_request(request):
    size = request.POST.get('size')
    model_name = request.POST.get('model_name')
    data = {'message': f'Added to cart: {model_name}, Size: {size}'}

    if not request.user.is_authenticated:
        if 'cart' not in request.session:
            request.session['cart'] = []
        try:
            product = Product.objects.get(model_name=model_name)
            request.session['cart'].append({'product': product.model_name,
                                            'size': size})
            request.session.save()
        except:
            data = {'message': 'Sorry, for some reason this item is not available'}
    else:
        pass

    return JsonResponse(data)
