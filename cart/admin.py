from django.contrib import admin
from .models import *

admin.site.register(ShippingMethod)


class OrderAdmin(admin.ModelAdmin):
    readonly_fields=('user_info','shipping_method','total','products')

    fieldsets = (
            ('Dane dostawy:', {'fields': ('user_info',)}),
            ('Dane zamówienia:', {'fields': ('shipping_method','total')}),
            ('Zamówienie:', {'fields': ('products',)}),
    )

admin.site.register(Order, OrderAdmin)
