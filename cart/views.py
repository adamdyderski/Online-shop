from django.contrib import messages
from django.core.urlresolvers import reverse_lazy,reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import TemplateView
from django.template.loader import render_to_string

from shop_app.models import Product
from .models import ShippingMethod, Order, OrderProduct
from .forms import ShippingMethodForm
from decimal import Decimal

def add_or_update(request, product_pk):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product = get_object_or_404(Product, pk=product_pk)
        add_quantity = int(request.POST.get("quantity", 1))

        if product.quantity < add_quantity:
            messages.info(request, 'Niestety, obecnie dostępnych sztuk: ' + str(product.quantity))
        elif add_quantity > 0 :
            if product_pk in cart:
                messages.success(request, 'Zaktualizowano koszyk!')
            else:
                messages.success(request, 'Dodano do koszyka!')
            cart[str(product.pk)] = add_quantity
            request.session['cart'] = cart
        else:
            messages.info(request, 'Podają poprawną ilość większą niż 0.')

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
        context['shipping_method'] = self.shipping_method = self.get_shipping_object();
        context['cart'] = self.cart = self.request.session.get('cart', {})
        context['products'] = self.products = self.get_cart_products()
        context['subtotal'], context['total'] = self.get_cart_price()
        return context

    def get_cart_price(self, subtotal = 0):
        for product in self.products:
            subtotal += product.price * self.cart[str(product.pk)]
        total = subtotal + self.shipping_method.price
        self.request.session['total'] = str(total)
        return subtotal, total

    def get_shipping_object(self):
        shipping_method_pk = int(self.request.session.get('shippingmethod', 1))
        shipping_method_obj = ShippingMethod.objects.get(pk=shipping_method_pk)
        return shipping_method_obj

    def get_cart_products(self):
        return Product.objects.filter(pk__in=self.cart)


def set_shipping_method(request):
    if request.method == 'POST':
        request.session['shippingmethod'] = int(request.POST.get("shippingmethod", 1))
        messages.success(request, 'Sposób wysyłki został zmieniony!')

    return HttpResponseRedirect(reverse_lazy('cart:show'))


def order(request):

    if request.user.is_authenticated():
        # dane z koszyka
        cart = request.session.get('cart', {})
        total = request.session.get('total', 0)
        shipping_method_pk = int(request.session.get('shippingmethod', 1))

        # nowe zamównienie
        order = Order()
        order.user = request.user
        order.shipping_method = ShippingMethod.objects.get(pk=shipping_method_pk)
        order.total = Decimal(request.session.get('total'))
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
        order_products = OrderProduct.objects.filter(order=order)
        for op in order_products:
            p = op.product
            p.quantity -= op.quantity
            p.save()

        # wyczyszczenie sesji
        del request.session['cart']
        del request.session['total']

        if 'shippingmethod' in request.session:
            del request.session['shippingmethod']

        # wysłanie maila
        title = 'Zamówienie nr '+ str(order.pk)
        url = request.build_absolute_uri(reverse('accounts:orders'))
        html_message = render_to_string('cart/order_confirmation.html', { 'order': order, 'order_products': order_products, 'link': url })
        request.user.email_user(title, '', html_message=html_message)

        messages.success(request, 'Zamówienie nr ' + str(order.pk) + ' zostało przyjęte do realizacji!')
        return HttpResponseRedirect(reverse_lazy('accounts:orders'))
    else:
        messages.info(request, 'Aby złożyć zamówienie, musisz się zalogować!')
        return HttpResponseRedirect(reverse_lazy('accounts:login'))
