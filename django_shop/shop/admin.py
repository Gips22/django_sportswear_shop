from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}  # cоздание слага на основе атрибута name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'price', 'available', 'get_html_photo']
    list_filter = ['available']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('title',)}  # cоздание слага на основе атрибута title
    search_fields = ['title']

    #  метод для отображения миниатюр в админке
    def get_html_photo(self, object):  # object тут ссылается на запись из таблицы (ЭК модели Product)
        if object.image:
            return mark_safe(
                f"<img src='{object.image.url}' width=65>")  # ф-ия mark_safe позволяет не экранировать то, что мы в нее передаем

    get_html_photo.short_description = 'Миниатюра '
