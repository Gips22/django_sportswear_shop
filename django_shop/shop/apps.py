from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
    verbose_name = 'Магазин спортивной одежды'  # это имя может быть использовано в разных модулях Джанго, в том числе для отображения в админке
                                                # сработает только если мы зарегистрируем наше приложение в settings  с использованием ShopConfig