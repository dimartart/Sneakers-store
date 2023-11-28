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
        self.request.session['username'] = self.request.user.username
        return redirect('base')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'lifeplan/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title="Log In")
        return dict(list(context.items()) + list(mixin_context.items()))

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.session['username'] = self.request.user.username
        return response

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

    if request.user.is_authenticated:
        username = request.session.get('username')
        user_order, created = Order.objects.get_or_create(client_username=username, is_paid=False)
        try:
            all_products_in_current_cart = [(object.product, object.size_of_product) for object in ProductInOrder.objects.filter(order=user_order)]
            total_price = user_order.total_price
            context['total_price'] = total_price
            context["all_products_in_current_cart"] = all_products_in_current_cart
        except:
            pass
    else:
        try:
            products_from_session = request.session['cart']
            all_products_from_db = Product.objects.all()
            l_prices = []
            for dct in products_from_session:
                dct['product'] = all_products_from_db.get(model_name=dct['model_name'])
                l_prices.append(dct['product'].price)
            context['total_price'] = sum(l_prices)
            context['products_from_session'] = products_from_session
            request.session.save()
        except:
            pass

    return render(request, 'lifeplan/cart.html', context=context)


def handle_ajax_request(request):
    size = request.POST.get('size')
    model_name = request.POST.get('model_name')
    data = {'message': f'Added to cart: {model_name}, Size: {size}'}

    if not request.user.is_authenticated:
        product_dct = {'model_name': model_name, 'size': size}
        if 'cart' not in request.session:
            request.session['cart'] = []
        try:
            if product_dct not in request.session['cart']:
                request.session['cart'].append({'model_name': model_name,
                                                'size': size})
                request.session.save()
            else:
                data = {'message': 'This item is already in your cart'}
        except:
            data = {'message': 'Sorry, for some reason this item is not available'}

    else:
        username = request.session.get('username')
        print(username)
        user_order, created = Order.objects.get_or_create(client_username=username, is_paid=False)
        product = Product.objects.get(model_name=model_name)
        try:
            ProductInOrder.objects.get(order=user_order, product=product, size_of_product=size)
            data = {'message': 'This item is already in your cart'}

        except:
            user_order.total_price += product.price
            user_order.items_amount += 1
            user_order.save()
            ProductInOrder.objects.create(order=user_order, product=product, size_of_product=size)

    return JsonResponse(data)


def remove_from_cart(request):
    product_unique_key = request.POST.get('product_unique_key')
    model_name, size = product_unique_key.split('&')
    if request.user.is_authenticated:
        product = Product.objects.get(model_name=model_name)
        username = request.session.get('username')
        user_order = Order.objects.get(client_username=username, is_paid=False)

        user_order.total_price -= product.price
        user_order.items_amount -= 1
        user_order.save()

        product_in_cart = ProductInOrder.objects.get(order=user_order, product=product, size_of_product=size)
        product_in_cart.delete()
        total_price = user_order.total_price

    else:
        for dct in request.session['cart']:
            values = dct.values()
            if model_name in values and size in values:
                request.session['cart'].remove(dct)
                request.session.save()
                break
        total_price = get_total_price(request)
    return JsonResponse({'message': f'{total_price} kc'})


def get_total_price(request):
    l_prices = []
    for dct in request.session['cart']:
        l_prices.append(Product.objects.get(model_name=dct['model_name']).price)
    return sum(l_prices)


