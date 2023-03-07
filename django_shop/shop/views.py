from loguru import logger
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, FormView, DetailView

from .forms import RegisterUserForm, LoginUserForm, FeedbackForm, ReviewForm
from .models import *
from .utils import DataMixin
from cart.forms import CartAddProductForm

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB")


class ShopHome(DataMixin, ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # вызываем родительский метод, чтобы получить базовый контекст
        context['title'] = "Главная"  # добавляем к контексту свои данные, полученные с помощью метода get_user_context
        return dict(list(context.items()))

    def get_queryset(self):
        """Добавляем для оптимизации нагрузки на БД. Благодаря методу select_related у нас происходит
        жадная, а не ленивая загрузка связанных данных  по внешнему FK. В моем случае я уменьшаю количество запросов
        по категориям на главной странице с 11 до 5 (так как в каждом товаре указывается категория)."""
        return Product.objects.all().select_related('category')


class ProductDetailView(DataMixin, DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'shop/product/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        context['review_form'] = ReviewForm()
        context['cart_product_form'] = CartAddProductForm()
        context = self.get_user_context(**context)
        return context

    def post(self, request, category_slug, slug):
        product = self.get_object()
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            cleaned_form = review_form.cleaned_data
            author_name = "Анонимный пользователь"
            Review.objects.create(
                product=product,
                author=author_name,
                rating=cleaned_form['rating'],
                text=cleaned_form['text']
            )
            return redirect('shop:product_detail', category_slug=category_slug, slug=slug)

        context = self.get_context_data()
        context['review_form'] = review_form
        return self.render_to_response(context)


class ShopCategory(DataMixin, ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'
    allow_empty = False  # генерация ошибки 404 если  нет товаров в категории

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['products'][0].category).upper()
        return dict(list(context.items()))

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['category_slug'])


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'shop/product/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Регистрация')
        context['form_first'] = RegisterUser.form_class
        return dict(list(context.items()) + list(user_context.items()))

    def form_valid(self, form):
        """Встроенный метод который вызывается при успешной регистрации.
        Нужен чтобы зарегистрированного пользователя автоматически авторизовывали.
        Отличие от атрибута success_url в том, что через переменную мы не можем
        после успешной регистрации сразу авторизовать, а также  переменную можно только статический
        адрес указать. Если ссылка формируется динамически - только метод подойдет.
        К примеру, Если я например делаю сайт, где у зарегистрированного пользователя
        есть личная страница,  и я хочу что бы она была по адресу mysite/accounts/<никнейм пользователя>"""
        user = form.save()  # самостоятельно сохраняем пользователя в нашу модель в БД.
        login(self.request, user)  # функция для авторизации пользователя
        return redirect('shop:product_list')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm  # тут мы указываем свою кастомную форму. Изначально пользовались встроенной - класс AutenticationForm
    template_name = 'shop/product/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Войти')
        return dict(list(context.items()) + list(user_context.items()))

    def get_success_url(self):
        return reverse_lazy('shop:product_list')


class FeedbackFormView(DataMixin, FormView):
    form_class = FeedbackForm
    template_name = 'shop/product/feedback.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Обратная связь')
        context['form_feedback'] = FeedbackFormView.form_class
        return dict(list(context.items()) + list(user_context.items()))

    def form_valid(self, form):
        logger.debug(form.cleaned_data)  # если форма заполнена корректно, то при отправке логируем данные из формы
        return redirect('shop:product_list')


def about(request):
    return render(request, 'shop/product/about.html')


def logout_user(request):
    logout(request)  # стандартная ф-ия Джанго для выхода из авторизации
    return redirect('shop:login')
