from .models import Category

def menu_processor(request):
    categories = Category.objects.order_by('name')
    cart_count = len(request.session.get('cart', {}))        
    return {'categories': categories, 'cart_count': cart_count}