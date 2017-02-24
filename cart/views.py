from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View

from shop_app.models import Product

def add(request, product_pk):
    
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_pk)
        add_quantity = int(request.POST.get("quantity", 1))

        if product.quantity < add_quantity:
            messages.info(request, 'Niestety, obecnie dostępnych sztuk: ' + str(product.quantity))
        else:
            cart = request.session.get('cart', {})
            cart.update(product_pk=add_quantity)
            request.session['cart'] = cart
            messages.success(request, 'Dodano do koszyka!')

    return HttpResponseRedirect(reverse_lazy('shop_app:details', kwargs={'pk': product_pk}))
