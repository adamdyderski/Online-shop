from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import TemplateView

from shop_app.models import Product


def add(request, product_pk):
    
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_pk)
        add_quantity = int(request.POST.get("quantity", 1))

        if product.quantity < add_quantity:
            messages.info(request, 'Niestety, obecnie dostępnych sztuk: ' + str(product.quantity))
        else:
            cart = request.session.get('cart', {})
            cart[str(product.pk)] = add_quantity
            request.session['cart'] = cart
            messages.success(request, 'Dodano do koszyka!')

    return HttpResponseRedirect(reverse_lazy('shop_app:details', kwargs={'pk': product_pk}))

def remove(request, product_pk):
    cart = request.session.get('cart', {})
    
    if product_pk in cart:
        del cart[product_pk]
        request.session['cart'] = cart
        messages.success(request, 'Usunięto z koszyka!')

    return HttpResponseRedirect(reverse_lazy('cart:show'))

class Show(View):
    template_name = 'cart/show_cart.html'

    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart', {})
        products = Product.objects.filter(pk__in=cart)
        return render(request, self.template_name, context={'products': products, 'cart': cart}) 
