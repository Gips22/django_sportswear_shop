from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, FormView
from .forms import RegisterUserForm, LoginUserForm, FeedbackForm, ReviewForm
from .models import *
from cart.forms import CartAddProductForm
from cart.views import cart_detail
from decimal import Decimal

categories = Category.objects.all()


class ShopHome(ListView):
    paginate_by = 6
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context[
            'categories'] = categories 
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
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html',
                  {'product': product, 'category': category, 'cart_product_form': cart_product_form})


# def product_detail(request, category_slug, slug):
#     category = get_object_or_404(Category, slug=category_slug)
#     product = get_object_or_404(Product, category_id=category.id, slug=slug)
#     if request.method == 'POST':
#         review_form = ReviewForm(request.POST)
#
#         if review_form.is_valid():
#             cf = review_form.cleaned_data
#
#             author_name = "Anonymous"
#             Review.objects.create(
#                 product=product,
#                 author=author_name,
#                 rating=cf['rating'],
#                 text=cf['text']
#             )
#         return redirect('shop:product_detail', category_slug=category_slug, slug=slug)
#     else:
#         review_form = ReviewForm()
#         cart_product_form = CartAddProductForm()
#         return render(request, 'product/detail.html', {'product': product, 'review_form': review_form, 'cart_product_form': cart_product_form})

class ShopCategory(ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'
    allow_empty = False  # генерация ошибки 404 если  нет товаров в категории

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['products'][0].category).upper()
        context[
            'categories'] = categories  # тут не оч понял почему нельяза переменную сategories со списком категорий из модели объявить прямо в классе, а нужно объявлять вне класса (сверху)
        return context

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['category_slug'])


def about(request):
    return render(request, 'shop/product/about.html')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'shop/product/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context[
            'categories'] = categories  # тут не оч понял почему нельяза переменную сategories со списком категорий из модели объявить прямо в классе, а нужно объявлять вне класса (сверху)
        return context

    def form_valid(self, form):
        """Встроенный метод который вызывается при успешной регистрации.
        Нужен чтобы зарегистрированного пользователя автоматически авторизовывали"""
        user = form.save()  # самостоятельно сохраняем пользователя в нашу модель в БД.
        login(self.request, user)  # функция для авторизации пользователя
        return redirect('shop:product_list')


# def register(request):
#     return render(request, 'shop/product/about.html')


class LoginUser(LoginView):
    form_class = LoginUserForm  # тут мы указываем свою кастомную форму. Изначально пользовались встроенной - класс AutenticationForm
    template_name = 'shop/product/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Войти'
        return context

    def get_success_url(self):
        return reverse_lazy('shop:product_list')


# def login(request):
#     return render(request, 'shop/product/login.html')

def logout_user(request):
    logout(request)  # стандартная ф-ия Джанго для выхода из авторизации
    return redirect('shop:login')


class FeedbackFormView(FormView):
    form_class = FeedbackForm
    template_name = 'shop/product/feedback.html'
    success_url = reverse_lazy('shop:product_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Форма обратной связи'
        return context

    def form_valid(self, form):
        print(form.cleaned_data)  # если форма заполнена корректно, то при отправке печатаем в консоль данные из формы
        return redirect('shop:product_list')
