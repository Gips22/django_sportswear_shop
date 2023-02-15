from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)  # сортировка применяется и в отображении в админке и в шаблонах
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'

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
        verbose_name = 'Товары'  # отображение названия в админке
        verbose_name_plural = 'Товары'  # отображение названия в админке
        ordering = ('title',)

    def __str__(self):
        return self.title

    # self ссылка на ЭК модели. Через self обращаемся к нужному атрибуту для формирования динамического url и использования в шаблонах.
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.category.slug,
                                                    self.slug])  # c помощью reverse формируем маршурут с именем shop:product_detail, для этого дополнитнительно  передаем нужные параметры

    def get_average_review_score(self):
        average_score = 0.0
        if self.reviews.count() > 0:
            total_score = sum([review.rating for review in self.reviews.all()])
            average_score = total_score / self.reviews.count()
        return round(average_score, 1)


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
