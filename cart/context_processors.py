
def cart_processor(request):
    cart = request.session.get('cart', {})
    return {'cart': cart, 'cart_count': len(cart)}
