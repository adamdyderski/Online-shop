from .models import ShippingMethod, Product
from decimal import Decimal
from django.shortcuts import get_object_or_404

class Cart(object):

    def __init__(self, request):
        """
        Inicjalizacja koszyka
        """
        # sesja
        self.session = request.session
        self.session_cart = self.session.get('cart', {})
        self.session_shipping_method = self.session.get('shippingmethod', 1)
        
        # obiekty
        self.products = Product.objects.filter(pk__in=self.session_cart)
        self.shipping_method = ShippingMethod.objects.get(pk=int(self.session_shipping_method))

    def get_subtotal_price(self):
        """
        Kwota koszyka
        """
        prices = [product.price * self.session_cart[str(product.pk)] for product in self.products]
        return Decimal(sum(prices))

    def get_total_price(self):
        """
        Kwota zamówienia
        """
        return Decimal(self.get_subtotal_price() + self.shipping_method.price)

    def set_shipping_method(self, value):
        """
        Sposób wysyłki
        """
        self.session_shipping_method = value
        self.save()

    def add_or_update(self, pk, quantity):
        """
        Dodawanie oraz aktualizacja produktów w koszyku
        """
        product = get_object_or_404(Product, pk=pk)

        if quantity <= 0:
            success, message = False, 'Podają poprawną ilość większą niż 0.'
        elif product.quantity < quantity:
            success, message = False, 'Niestety, obecnie dostępnych sztuk: ' + str(product.quantity)
        elif pk in self.session_cart:
            success, message = True, 'Zaktualizowano koszyk!'
        else:
            success, message = True, 'Dodano do koszyka!'

        self.session_cart[str(pk)] = int(quantity)
        self.save()

        return success, message

    def remove(self, pk):
        """
        Usuwanie z koszyka
        """
        del self.session_cart[pk]
        self.save()

    def save(self):
        """
        Zapisywanie
        """
        self.session['cart'] = self.session_cart
        self.session['shippingmethod'] = self.session_shipping_method
        self.session.modified = True
