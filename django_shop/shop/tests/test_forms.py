from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate
from shop.forms import RegisterUserForm, LoginUserForm, FeedbackForm, ReviewForm
from shop.models import Product, Review, Category


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

    def test_login_view_valid(self):
        """Тест успешной авторизации через view"""
        response = self.client.post(reverse('shop:login'), data=self.valid_data,
                                    follow=True)  # follow=True означает, что приложение должно следовать любым редиректам, которые могут быть выполнены в процессе выполнения запроса.
        user = authenticate(username=self.valid_data['username'], password=self.valid_data['password'])
        self.assertTrue(user.is_authenticated)
        self.assertRedirects(response, reverse('shop:product_list'))

    def test_login_view_invalid(self):
        """Тест неуспешной авторизации через view"""
        response = self.client.post(reverse('shop:login'), data=self.invalid_data, follow=True)
        user = authenticate(username=self.invalid_data['username'], password=self.invalid_data['password'])
        self.assertIsNone(user)
        self.assertContains(response,
                            'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.')


class FeedbackFormTest(TestCase):
    # НЕВАЛИДНЫЙ ТЕСТ ИЗ-ЗА КАПТЧИ
    # def test_valid_feedback_form_submission(self):
    #     form_data = {
    #         'name': 'Test2 User',
    #         'email': 'test2@example.com',
    #         'content': 'Test message',
    #         'capatcha': 'PASSED',
    #     }
    #     form = FeedbackForm(data=form_data)
    #     self.assertTrue(form.is_valid())

    def test_invalid_feedback_form(self):
        form_data = {
            'name': 'Test User',
            'email': 'invalid-email',
            'content': '',
            'capatcha': 'FAILED',
        }
        form = FeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('content', form.errors)

    def test_feedback_form_view(self):
        response = self.client.get(reverse('shop:feedback'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/feedback.html')

        form = response.context['form']
        self.assertIsInstance(form, FeedbackForm)

    # НЕВАЛИДНЫЙ ТЕСТ ИЗ-ЗА КАПТЧИ
    # def test_valid_feedback_form_submission(self):
    #     # form_data = {
    #     #     'name': 'Test User',
    #     #     'email': 'test@example.com',
    #     #     'content': 'Test message',
    #     #     'capatcha': 'PASSED',
    #     # }
    #     # response = self.client.post(reverse('shop:feedback'), data=form_data)
    #     # # self.assertRedirects(response, reverse('shop:product_list'))
    #     # self.assertRedirects(response, reverse('shop:product_list') + '?sent=True')
    #     # # self.assertEqual(response, reverse('shop:product_list') + '?sent=True')

    def test_invalid_feedback_form_submission(self):
        form_data = {
            'name': 'Test User',
            'email': 'invalid-email',
            'content': '',
            'capatcha': 'FAILED',
        }
        response = self.client.post(reverse('shop:feedback'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/feedback.html')


class ReviewFormTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name='TestCategory', slug='test-category')
        self.product = Product.objects.create(
            category=category,
            title='TestProduct',
            slug='test-product',
            price=100,
            available=True
        )

    def test_valid_review_form_submission(self):
        form_data = {
            'text': 'Test review text',
            'rating': 4
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

        review = form.save(commit=False)
        review.product = self.product
        review.author = 'Test User'
        review.save()

        self.assertEqual(Review.objects.count(), 1)
        saved_review = Review.objects.first()
        self.assertEqual(saved_review.text, 'Test review text')
        self.assertEqual(saved_review.rating, 4)
        self.assertEqual(saved_review.product, self.product)
        self.assertEqual(saved_review.author, 'Test User')
