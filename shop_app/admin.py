from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    empty_value_display = '-'

    list_display = ('name','categories','quantity','price')
    list_filter = ('category__name', 'price','quantity')
    search_fields = ['name']



admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
