from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

from .models import Review


class RegisterUserForm(UserCreationForm):
    """Форма регистрации пользователей"""
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}), min_length=8,
                                error_messages={'min_length': 'Пароль должен быть длиной не менее 8 символов'})
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password2

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError('Пароль должен содержать не менее 8 символов.')
        if password1.isdigit():
            raise forms.ValidationError('Пароль должен содержать хотя бы один символ, кроме цифр.')
        return password1

    class Meta:
        model = User  # связываем форму с встроенной моделью User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    """Форма для аутентификации потльзователей"""
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class FeedbackForm(forms.Form):
    """Форма обратной связи"""
    name = forms.CharField(label='Имя', max_length=100)
    email = forms.EmailField(label='Email')
    content = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'cols': 30, 'rows': 4}))
    capatcha = CaptchaField(label='Введите каптчу с картинки')


class ReviewForm(forms.ModelForm):
    """Форма для оставления отзыва на товар"""

    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(
                attrs={'class': 'form-control shadow px-2',
                       'rows': 6
                       }
            ),
            'rating': forms.RadioSelect
        }
