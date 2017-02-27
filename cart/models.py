from django.db import models

class ShippingMethod(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nazwa")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Cena")
    days = models.IntegerField(verbose_name="Przewidywany czas dostawy (dni)")

    def __str__(self):
        return '{} - {} zł ({} dni)'.format(self.name,self.price,self.days)

    class Meta:
        verbose_name = "Sposób wysyłki"
        verbose_name_plural = "Sposoby wysyłki"
