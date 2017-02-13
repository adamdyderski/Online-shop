from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nazwa")
    description = models.TextField(max_length=4000, blank=True, verbose_name="Opis")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Cena")
    quantity = models.IntegerField(default=0, verbose_name="Ilość")
    image = models.FileField(default="no_photo.png",verbose_name="Zdjęcie")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Produkt"
        verbose_name_plural = "Produkty"