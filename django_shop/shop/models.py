from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_detail', args = [self.category.slug, self.slug])

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

