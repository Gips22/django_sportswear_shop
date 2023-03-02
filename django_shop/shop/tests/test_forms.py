from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate
from shop.forms import RegisterUserForm, LoginUserForm


class RegisterUserFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }

    def test_form_valid(self):
        form = RegisterUserForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_email(self):
        invalid_data = self.valid_data.copy()
        invalid_data['email'] = 'invalidemail'
        form = RegisterUserForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email',
                      form.errors)  # Если ключ 'email' есть в form.errors, значит, при валидации формы возникла ошибка в поле 'email'.

    def test_form_invalid_passwords(self):
        invalid_data = self.valid_data.copy()
        invalid_data['password2'] = 'differentpassword'
        form = RegisterUserForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_form_username_already_exists(self):
        User.objects.create_user(username=self.valid_data['username'], email=self.valid_data['email'],
                                 password=self.valid_data['password1'])
        form = RegisterUserForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


class LoginUserFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.valid_data = {
            'username': 'testuser',
            'password': 'testpass'
        }
        self.invalid_data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }

    def test_login_form_valid(self):
        """Тест успешной авторизации"""
        form = LoginUserForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        """Тест неуспешной авторизации"""
        form = LoginUserForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())
        # self.assertIn('Пожалуйста, введите правильные имя пользователя и пароль', form.errors['__all__'])

    def test_login_view_valid(self):
        """Тест успешной авторизации через view"""
        response = self.client.post(reverse('shop:login'), data=self.valid_data, follow=True)
        user = authenticate(username=self.valid_data['username'], password=self.valid_data['password'])
        self.assertTrue(user.is_authenticated)
        self.assertRedirects(response, reverse('shop:product_list'))

    def test_login_view_invalid(self):
        """Тест неуспешной авторизации через view"""
        response = self.client.post(reverse('shop:login'), data=self.invalid_data, follow=True)
        user = authenticate(username=self.invalid_data['username'], password=self.invalid_data['password'])
        self.assertIsNone(user)
        self.assertContains(response, 'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.')
