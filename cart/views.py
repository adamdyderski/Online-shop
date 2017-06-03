from django.contrib import messages
from django.core.urlresolvers import reverse_lazy,reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView
from django.template.loader import render_to_string

from .cart import Cart
from shop_app.models import Product
from .models import ShippingMethod, Order, OrderProduct
from .forms import ShippingMethodForm


def add_or_update(request, product_pk):

    if request.method == 'POST':
        quantity = request.POST.get('quantity', 1)
        cart = Cart(request)
        success, message = cart.add_or_update(product_pk, int(quantity))

        if success:
            messages.success(request, message)
        else:
            messages.info(request, message)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove(request, product_pk):
    cart = Cart(request)

    if product_pk in cart.session_cart:
        cart.remove(product_pk)
        messages.success(request, 'Usunięto z koszyka!')

    return HttpResponseRedirect(reverse_lazy('cart:show'))


class ShowCart(TemplateView):
    template_name = 'cart/show_cart.html'

    def get_context_data(self, **kwargs):
        context = super(ShowCart, self).get_context_data(**kwargs)
        context['shippingmethodform'] = ShippingMethodForm(self.request)
        context['cart'] = Cart(self.request)
        return context


def set_shipping_method(request):

    if request.method == 'POST':
        value = request.POST.get("shippingmethod", 1)
        cart = Cart(request)
        cart.set_shipping_method(value)
        messages.success(request, 'Sposób wysyłki został zmieniony!')

    return HttpResponseRedirect(reverse_lazy('cart:show'))


def order_create(request):

    if request.user.is_authenticated():

        # dane z koszyka
        cart = Cart(request)

        # nowe zamównienie
        order = Order()
        order.user = request.user
        order.shipping_method = ShippingMethod.objects.get(pk=cart.shipping_method.pk)
        order.total = cart.get_total_price()
        order.save()

        # produkty do zamówienia
        try:
            for key, value in cart.session_cart.items():
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
