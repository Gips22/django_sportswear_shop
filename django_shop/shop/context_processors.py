from .models import Category


def shop(request):
    categories = Category.objects.all()
    return {'categories': categories}
