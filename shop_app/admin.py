from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    empty_value_display = '-'

    list_display = ('name','thumb','categories','quantity','price',)
    list_filter = ('category__name', 'price','quantity')
    search_fields = ['name']
    
    class Media:
        css = {'all': ('admin/css/v_align_table.css',)}

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
