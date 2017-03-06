from .models import Category


def categories_processor(request):
    categories = Category.objects.order_by('name')
    return {'categories': categories}
