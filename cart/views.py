from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import TemplateView

from shop_app.models import Product
from .models import ShippingMethod, Order, OrderProduct
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
        context['shippingmethodform'] = ShippingMethodForm(self.request)

        context['cart'] = self.cart = self.request.session.get('cart', {})
        context['products'] = self.products = Product.objects.filter(pk__in=self.cart)
        context['shipping_cost'] = shipping_cost = self.get_shipping_cost()
        context['subtotal'] = self.cart_price()
        context['total'] = self.cart_price(shipping_cost)
        return context

    def cart_price(self, price = 0):
        for product in self.products:
            price += product.price * self.cart[str(product.pk)]
        return price

    def get_shipping_cost(self):
        shipping_method_pk = int(self.request.session.get('shippingmethod', 1))
        shipping_method = ShippingMethod.objects.get(pk=shipping_method_pk)
        return shipping_method.price


def set_shipping_method(request):
    if request.method == 'POST':
        request.session['shippingmethod'] = int(request.POST.get("shippingmethod", 1))
        messages.success(request, 'Sposób wysyłki został zmieniony!')

    return HttpResponseRedirect(reverse_lazy('cart:show'))


def order(request):
    if request.user.is_authenticated():

        # dane z koszyka
        cart = request.session.get('cart', {})
        shipping_method_pk = int(request.session.get('shippingmethod', 1))

        # nowe zamównienie
        order = Order()
        order.user = request.user
        order.shipping_method = ShippingMethod.objects.get(pk=shipping_method_pk)
        order.total = 1
        order.save()

        # produkty do zamówienia
        try:
            for key, value in cart.items():
                op = OrderProduct()
                op.order = order
                op.product = Product.objects.get(pk=int(key))
                op.quantity = value
                op.clean()
                op.save()
        except Exception as e:
            order.delete()
            messages.error(request, e)
            return HttpResponseRedirect(reverse_lazy('cart:show'))

        # aktualizacja stanu magazynu
        for op in OrderProduct.objects.filter(order=order):
            p = op.product
            p.quantity -= op.quantity
            p.save()

        # wyczyszczenie sesji
        del request.session['cart']

        if 'shippingmethod' in request.session:
            del request.session['shippingmethod']

        return HttpResponseRedirect(reverse_lazy('shop_app:home'))
    else:
        messages.info(request, 'Aby złożyć zamówienie, musisz się zalogować!')
        return HttpResponseRedirect(reverse_lazy('accounts:login'))
