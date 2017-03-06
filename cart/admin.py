from django.contrib import admin
from .models import *



# class OrderProductInline(admin.TabularInline):
#     readonly_fields = ['product','product','quantity']
#     model = OrderProduct
#     extra = 0
#     can_delete = False
#     verbose_name = 'Zamówiony Produkt'
#     verbose_name_plural = 'Zamówione produkty'

class OrderAdmin(admin.ModelAdmin):
    readonly_fields=('user_info','shipping_method','total','products')

    fieldsets = (
            (None, {'fields': ('status',)}),
            ('Dane dostawy:', {'fields': ('user_info',)}),
            ('Dane zamówienia:', {'fields': ('shipping_method','total')}),
            ('Zamówienie:', {'fields': ('products',)}),
    )

    # inlines = [
    #     OrderProductInline,
    # ]

class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ('name','price','days')
    list_filter = ('price', 'days')
    search_fields = ['name']

admin.site.register(Order, OrderAdmin)
admin.site.register(ShippingMethod, ShippingMethodAdmin)
