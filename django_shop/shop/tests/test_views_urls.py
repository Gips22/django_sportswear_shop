from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from shop.models import Category, Product, Review
from shop.forms import ReviewForm, RegisterUserForm, LoginUserForm, FeedbackForm
from cart.forms import CartAddProductForm


class TestShopHome(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Category', slug='category')
        self.product = Product.objects.create(
            category=self.category,
            title='Product',
            slug='product',
            image='image.jpg',
            description='Product description',
            price=10.99,
        )

    def test_get_queryset(self):
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['products'], [self.product],
                                 transform=lambda x: x)  # через lambda идет преобразование в  [<Product: Product>]

    def test_context_data(self):
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'Главная')
        self.assertIn('products', response.context)
        self.assertTrue(response.context['products'].count() > 0)

    def test_category_model_get_absolute_url(self):
        self.assertEqual(self.category.get_absolute_url(), '/category/category/')

    def test_product_model_get_absolute_url(self):
        self.assertEqual(self.product.get_absolute_url(), '/category/category/product')

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('shop:product_list'))
        self.assertTemplateUsed(response, 'shop/product/list.html')


class ProductDetailViewTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test category', slug='test-category')
        self.product = Product.objects.create(
            category=self.category,
            title='Product',
            slug='product',
            image='image.jpg',
            description='Product description',
            price=10.99,
        )
        self.review = Review.objects.create(
            product=self.product,
            author='Test author',
            rating=4,
            text='Test review text'
        )

        self.detail_url = reverse('shop:product_detail', args=[self.category.slug, self.product.slug])

    def test_detail_view_status_code(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template_used(self):
        response = self.client.get(self.detail_url)
        self.assertTemplateUsed(response, 'shop/product/detail.html')

    def test_detail_view_context_object_name(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.context['product'], self.product)

    def test_detail_view_context_review_form(self):
        response = self.client.get(self.detail_url)
        self.assertIsInstance(response.context['review_form'], ReviewForm)

    def test_detail_view_context_cart_product_form(self):
        response = self.client.get(self.detail_url)
        self.assertIsInstance(response.context['cart_product_form'],
                              CartAddProductForm)  # проверка типа объекта на соответствие заданному классу

    def test_detail_view_context_category(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.context['category'], self.category)

    def test_detail_view_context_user_authenticated(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.detail_url)
        self.assertEqual(response.context['user'], user)

    def test_detail_view_context_user_not_authenticated(self):
        response = self.client.get(self.detail_url)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_detail_view_post_valid_form(self):
        data = {
            'rating': 5,
            'text': 'Test review text'
        }
        response = self.client.post(self.detail_url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.product.reviews.count(), 2)


class ShopCategoryViewTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test category', slug='test-category')
        self.product1 = Product.objects.create(
            category=self.category,
            title='Product 1',
            slug='product-1',
            image='image1.jpg',
            description='Product 1 description',
            price=10.99,

        )
        self.product2 = Product.objects.create(
            category=self.category,
            title='Product 2',
            slug='product-2',
            image='image2.jpg',
            description='Product 2 description',
            price=19.99,
        )
        self.url = reverse('shop:product_list_by_category', args=[self.category.slug])

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('shop:product_list_by_category', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'shop/product/list.html')

    def test_view_returns_products_in_category(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['products']), 2)
        self.assertIn(self.product1, response.context['products'])
        self.assertIn(self.product2, response.context['products'])

    def test_view_title_contains_category_name(self):
        response = self.client.get(self.url)
        self.assertIn(str(self.category).upper(), response.context['title'])

    def test_view_raises_404_on_empty_category(self):
        empty_category = Category.objects.create(name='Empty category', slug='empty-category')
        url = reverse('shop:product_list_by_category', args=[empty_category.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TestRegisterUserView(TestCase):

    def setUp(self):
        self.url = reverse('shop:register')
        self.data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }

    def test_register_user_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/register.html')
        self.assertIsInstance(response.context['form'], RegisterUserForm)

    def test_register_user_view_post_success(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('shop:product_list'))
        user = User.objects.get(username=self.data['username'])
        self.assertEqual(user.email, self.data['email'])


class LoginUserTests(TestCase):
    def setUp(self):
        self.url = reverse('shop:login')
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )

    def test_login_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/login.html')
        self.assertIsInstance(response.context['form'], LoginUserForm)


class FeedbackFormViewTest(TestCase):

    def test_feedback_form_url_resolves_to_feedback_form_view(self):
        self.url = reverse('shop:feedback')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/feedback.html')
        self.assertIsInstance(response.context['form'], FeedbackForm)


class AboutViewTest(TestCase):

    def test_about_view_status_code(self):
        response = self.client.get(reverse('shop:about'))
        self.assertEqual(response.status_code, 200)

    def test_about_view_template(self):
        response = self.client.get(reverse('shop:about'))
        self.assertTemplateUsed(response, 'shop/product/about.html')


class LogoutUserViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_logout_user_view_redirects_to_login(self):
        response = self.client.get(reverse('shop:logout'))
        self.assertRedirects(response, reverse('shop:login'))

    def test_logout_user_view_logs_out_user(self):
        self.client.post(reverse('shop:login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertTrue('_auth_user_id' in self.client.session)
        self.client.get(reverse('shop:logout'))
        self.assertFalse('_auth_user_id' in self.client.session)
