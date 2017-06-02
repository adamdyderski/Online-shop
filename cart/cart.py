from .models import ShippingMethod, Product
from decimal import Decimal

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
        self.session_shipping_method = value
        self.save()

    def add_to_cart(self, pk, quantity):
        product = get_object_or_404(Product, pk=product_pk)
        self.session_cart[str(pk)] = int(quantity)
        self.session['cart'] = session_cart
        self.save()

    def save(self):
        self.session['cart'] = self.session_cart
        self.session['shippingmethod'] = self.session_shipping_method
        self.session.modified = True
