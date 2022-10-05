from .models import *


class DataMixin:
    """
    Mixin в данном случае не обязателен. Категории в контексте передаются в context_processors.
    Сделал для опыта, а также на будущее можно его дополнять.
    """
    paginate_by = 6  # класс представления нашей страницы со списком товаров наследуется от ListView, который
                     # в свою очередь автоматически передает в указанный шаблон 2 объекта: paginator и page_obj

    def get_user_context(self, **kwargs):
        context = kwargs
        categories = Category.objects.all()
        context['categories'] = categories
        return context
