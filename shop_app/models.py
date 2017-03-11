from django.db import models
from django.utils.safestring import mark_safe

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nazwa kategorii")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

class Product(models.Model):
    category = models.ManyToManyField(Category, verbose_name="Kategorie")
    name = models.CharField(max_length=50, verbose_name="Nazwa")
    description = models.TextField(max_length=4000, blank=True, verbose_name="Opis")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Cena")
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name="Ilość")
    image = models.FileField(default="no_photo.png",verbose_name="Zdjęcie")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Produkt"
        verbose_name_plural = "Produkty"

    def categories(self):
        return ", ".join([c.name for c in self.category.all()])
    categories.short_description = 'Kategorie'

    def thumb(self):
        if self.pk and self.image:
            return mark_safe('<img src="%s" width="70"/>' % self.image.url)
        else:
            return '-'
    thumb.short_description = 'Zdjęcie (podgląd)'
