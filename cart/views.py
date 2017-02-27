from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import TemplateView

from shop_app.models import Product
from .models import ShippingMethod
from .forms import ShippingMethodForm

def add_or_update(request, product_pk):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product = get_object_or_404(Product, pk=product_pk)
        add_quantity = int(request.POST.get("quantity", 1))

        if product.quantity < add_quantity:
            messages.info(request, 'Niestety, obecnie dostępnych sztuk: ' + str(product.quantity))
        else:
            if product_pk in cart:
                messages.success(request, 'Zaktualizowano koszyk!')
            else:
                messages.success(request, 'Dodano do koszyka!')

            cart[str(product.pk)] = add_quantity
            request.session['cart'] = cart

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove(request, product_pk):
    cart = request.session.get('cart', {})

    if product_pk in cart:
        del cart[product_pk]
        request.session['cart'] = cart
        messages.success(request, 'Usunięto z koszyka!')

    return HttpResponseRedirect(reverse_lazy('cart:show'))


class ShowCart(TemplateView):
    template_name = 'cart/show_cart.html'

    def get_context_data(self, **kwargs):
        context = super(ShowCart, self).get_context_data(**kwargs)
        # dane z sesji
        context['cart'] = self.cart = self.request.session.get('cart', {})
        context['shippingmethod'] = shippingmethod = int(self.request.session.get('shippingmethod', 1))
        # dane z bazy
        context['products'] = self.products = Product.objects.filter(pk__in=self.cart)
        context['shipping_cost'] = shipping_cost = ShippingMethod.objects.get(pk=shippingmethod).price

        context['shippingmethodform'] = ShippingMethodForm(self.request)

        context['subtotal'] = self.cart_price()
        context['total'] = self.cart_price(shipping_cost)
        return context

    def cart_price(self, price = 0):
        for product in self.products:
            price += product.price * self.cart[str(product.pk)]
        return price


def set_shipping_method(request):
    if request.method == 'POST':
        request.session['shippingmethod'] = int(request.POST.get("shippingmethod", 1))
        messages.success(request, 'Sposób wysyłki został zmieniony!')

    return HttpResponseRedirect(reverse_lazy('cart:show'))
