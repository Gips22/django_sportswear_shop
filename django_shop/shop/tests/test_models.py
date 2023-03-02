from django.test import TestCase
from django.urls import reverse
from shop.models import Category


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
