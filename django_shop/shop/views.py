from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import *


categories = Category.objects.all()


class ShopHome(ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['categories'] = categories # тут не оч понял почему нельяза переменную сategories со списком категорий из модели объявить прямо в классе, а нужно объявлять вне класса (сверху)
        return context

# def product_list(request, category_slug=None):
#     category = None
#     categories = Category.objects.all()
#     products = Product.objects.all()
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(category=category)
#     return render(request, 'shop/product/list.html',
#                   {
#                       'category': category,
#                       'categories': categories,
#                       'products': products
#                   })

def product_detail(request, category_slug, slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product/detail.html', {'product': product, 'category': category})

class ShopCategory(ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'
    allow_empty = False # генерация ошибки 404 если  нет товаров в категории

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['products'][0].category).upper()
        context['categories'] = categories # тут не оч понял почему нельяза переменную сategories со списком категорий из модели объявить прямо в классе, а нужно объявлять вне класса (сверху)
        return context

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['category_slug'])




def about(request):
    return render(request, 'shop/product/about.html')

def contact(request):
    return render(request, 'shop/product/contact.html')

class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = 'shop/product/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context['categories'] = categories  # тут не оч понял почему нельяза переменную сategories со списком категорий из модели объявить прямо в классе, а нужно объявлять вне класса (сверху)
        return context

# def register(request):
#     return render(request, 'shop/product/about.html')


def login(request):
    return render(request, 'shop/product/about.html')
