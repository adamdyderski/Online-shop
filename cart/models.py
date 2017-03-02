from django.db import models
from shop_app.models import Product
from accounts.models import User

class ShippingMethod(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nazwa")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Cena")
    days = models.IntegerField(verbose_name="Przewidywany czas dostawy (dni)")

    def __str__(self):
        return '{} - {} zł ({} dni)'.format(self.name,self.price,self.days)

    class Meta:
        verbose_name = "Sposób wysyłki"
        verbose_name_plural = "Sposoby wysyłki"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Użytkownik")
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.CASCADE, verbose_name="Sposób wysyłki")
    total = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Kwota zamówienia")
    STATUS = (
        (1, 'Oczekiwanie na realizację'),
        (2, 'W trakcie realizacji'),
        (3, 'Gotowe do wysyłki'),
        (4, 'Wysłano'),
    )
    status = models.IntegerField(default=1, choices=STATUS)

    def products(self):
        products = OrderProduct.objects.filter(order=self.pk)
        return '\n'.join([str(p) for p in products])
    products.short_description = 'Zamówione produkty'

    def user_info(self):
        u = []
        u.append(self.user.first_name)
        u.append(self.user.last_name)
        u.append(self.user.street)
        u.append(self.user.postcode)
        u.append(self.user.city)
        u.append(self.user.phone)
        return '{} {}\n{}\n{} {}\n{}'.format(*u)
    user_info.short_description = 'Dane użytkownika'


    def __str__(self):
        return 'Zamówienie nr {}'.format(self.pk)

    class Meta:
        verbose_name = "Zamówienie"
        verbose_name_plural = "Zamówienia"

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Zamówienie")
    product =  models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produkt")
    quantity = models.IntegerField(default=1, verbose_name="Ilość")

    def __str__(self):
        return '[ {} ] - {} ({} szt.)'.format(self.product.pk ,self.product, self.quantity)
