from django.test import TestCase
from django.urls import reverse
from shop.models import Category, Product


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')

    def test_create_category(self):
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(self.category.slug, 'test-category')

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Test Category')

    def test_category_get_absolute_url(self):
        url = reverse('shop:product_list_by_category', args=['test-category'])
        self.assertEqual(self.category.get_absolute_url(), url)

    def test_category_slug_unique(self):
        with self.assertRaises(Exception):
            Category.objects.create(name='Test Category 2', slug='test-category')

    def test_category_ordering(self):
        Category.objects.create(name='Category B', slug='category-b')
        Category.objects.create(name='Category A', slug='category-a')
        categories = Category.objects.order_by('name')
        self.assertEqual(list(categories), [categories[0], categories[1], self.category])

    def test_category_meta_verbose_name(self):
        self.assertEqual(Category._meta.verbose_name, 'Категории')

    def test_category_meta_verbose_name_plural(self):
        self.assertEqual(Category._meta.verbose_name_plural, 'Категории')


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            category=self.category,
            title='Atest Product',
            slug='atest-product',
            image='test-image.jpg',
            description='atest Description',
            price=9.99,
            available=True
        )

    def test_product_attributes(self):
        self.assertEqual(str(self.product), 'Atest Product')
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.title, 'Atest Product')
        self.assertEqual(self.product.slug, 'atest-product')
        self.assertEqual(self.product.image, 'test-image.jpg')
        self.assertEqual(self.product.description, 'atest Description')
        self.assertEqual(self.product.price, 9.99)
        self.assertTrue(self.product.available)

    def test_get_absolute_url(self):
        url = reverse('shop:product_detail', args=[self.category.slug, self.product.slug])
        self.assertEqual(self.product.get_absolute_url(), url)

    def test_get_average_review_score(self):
        self.assertEqual(self.product.get_average_review_score(), 0.0)

    def test_product_ordering(self):
        Product.objects.create(
            category=self.category,
            title='Product B',
            slug='product-b',
            image='test-image.jpg',
            description='Test Description',
            price=19.99,
            available=True
        )
        Product.objects.create(
            category=self.category,
            title='Product A',
            slug='product-a',
            image='test-image.jpg',
            description='Test Description',
            price=14.99,
            available=True
        )
        products = Product.objects.all()
        self.assertEqual(list(products), [self.product, products[1], products[2]])

    def test_default_available_value(self):
        product = Product.objects.create(
            category=self.category,
            title='Product C',
            slug='product-c',
            image='test-image.jpg',
            description='Test Description',
            price=29.99,
        )
        self.assertTrue(product.available)

    def test_product_connect_to_category(self):
        """Проверяем, что товар был создан успешно и связан с правильной категорией"""
        Product.objects.all().delete()
        category = Category.objects.create(name='Test2 Category', slug='test2-category')

        product = Product.objects.create(
            category=category,
            title='Test Product',
            slug='test-product',
            image='test-image.jpg',
            description='Test Description',
            price=9.99,
            available=True,
        )

        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(product.category, category)
        self.assertEqual(product.title, 'Test Product')
        self.assertEqual(product.slug, 'test-product')
        self.assertEqual(product.image, 'test-image.jpg')
        self.assertEqual(product.description, 'Test Description')
        self.assertEqual(product.price, 9.99)
        self.assertEqual(product.available, True)
