from django.test import TestCase
from django.urls import reverse
from shop.models import Category, Product


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
        self.assertQuerysetEqual(response.context['products'], [self.product], transform=lambda x: x)  # через lambda идет преобразование в  [<Product: Product>]

    def test_get_context_data(self):
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'Главная')

    def test_category_model_get_absolute_url(self):
        self.assertEqual(self.category.get_absolute_url(), '/category/category/')

    def test_product_model_get_absolute_url(self):
        self.assertEqual(self.product.get_absolute_url(), '/category/category/product')

#
# class TestShopCategory(TestCase):
#     def setUp(self):
#         self.category = Category.objects.create(name='Category', slug='category')
#         self.product = Product.objects.create(
#             category=self.category,
#             title='Product',
#             slug='product',
#             image='image.jpg',
#             description='Product description',
#             price=10.99,
#         )
#
#     def test_get_queryset(self):
#         response = self.client.get(reverse('shop:product_list_by_category', args=['category']))
#         self.assertEqual(response.status_code, 200)
#         self.assertQuerysetEqual(response.context['products'], ['<Product: Product>'])
#
#     def test_get_context_data(self):
#         response = self.client.get(reverse('shop:product_list_by_category', args=['category']))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.context['category'], self.category)
#         self.assertEqual(response.context['title'], 'Category')
#
#     def test_category_model_get_absolute_url(self):
#         self.assertEqual(self.category.get_absolute_url(), '/category/category/')
#
#     def test_product_model_get_absolute_url(self):
#         self.assertEqual(self.product.get_absolute_url(), '/category/category/product')
#
#
# class TestProductDetail(TestCase):
#     def setUp(self):
#         self.category = Category.objects.create(name='Category', slug='category')
#         self.product = Product.objects.create(
#             category=self.category,
#             title='Product',
#             slug='product',
#             image='image.jpg',
#             description='Product description',
#             price=10.99,
#         )
#
#     def test_get(self):
#         response = self.client.get(reverse('shop:product_detail', args=['category', 'product']))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.context['product'], self.product)
#         self.assertEqual(response.context['title'], 'Product')
#
#     def test_product_model_get_absolute_url(self):
#         self.assertEqual(self.product.get_absolute_url(), '/category/category/product')
