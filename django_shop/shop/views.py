from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, FormView
from .forms import RegisterUserForm, LoginUserForm, FeedbackForm, ReviewForm
from .models import *
from cart.forms import CartAddProductForm
from .utils import DataMixin


class ShopHome(DataMixin, ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        """Добавляем для оптимизации нагрузки на БД. Благодаря методу select_related у нас происходит
        жадная, а не ленивая загрузка связанных данных  по внешнему FK. В моем случае я уменьшаю количество запросов
        по категориям на главной странице с 11 до 5 (так как в каждом товаре указывается категория)."""
        return Product.objects.all().select_related('category')


def product_detail(request, category_slug, slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            cf = review_form.cleaned_data

            author_name = "Анонимный пользователь"
            Review.objects.create(
                product=product,
                author=author_name,
                rating=cf['rating'],
                text=cf['text']
            )
        return redirect('shop:product_detail', category_slug=category_slug, slug=slug)
    else:
        review_form = ReviewForm()
        cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html',
                  {'product': product, 'category': category, 'review_form': review_form,
                   'cart_product_form': cart_product_form})


class ShopCategory(DataMixin, ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'
    allow_empty = False  # генерация ошибки 404 если  нет товаров в категории

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['products'][0].category).upper())
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['category_slug'])


def about(request):
    return render(request, 'shop/product/about.html')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'shop/product/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        context['form_first'] = RegisterUser.form_class
        return dict(list(context.items()) + list(c_def.items()))

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
        c_def = self.get_user_context(title='Войти')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('shop:product_list')


def logout_user(request):
    logout(request)  # стандартная ф-ия Джанго для выхода из авторизации
    return redirect('shop:login')


class FeedbackFormView(DataMixin, FormView):
    form_class = FeedbackForm
    template_name = 'shop/product/feedback.html'
    success_url = reverse_lazy('shop:product_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        context['form_feedback'] = FeedbackFormView.form_class
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)  # если форма заполнена корректно, то при отправке печатаем в консоль данные из формы
        return redirect('shop:product_list')
