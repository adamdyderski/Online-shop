from django.contrib import admin
from .models import *
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse_lazy,reverse


# class OrderProductInline(admin.TabularInline):
#     readonly_fields = ['product','product','quantity']
#     model = OrderProduct
#     extra = 0
#     can_delete = False
#     verbose_name = 'Zamówiony Produkt'
#     verbose_name_plural = 'Zamówione produkty'

class OrderAdmin(admin.ModelAdmin):
    readonly_fields=('user','user_info','shipping_method','total','products')
    list_display = ('__str__','user','shipping_method','total','get_status')
    list_filter = ('shipping_method','status')
    search_fields = ['id']

    fieldsets = (
            (None, {'fields': ('status',)}),
            ('Dane dostawy:', {'fields': ('user','user_info',)}),
            ('Dane zamówienia:', {'fields': ('shipping_method','total')}),
            ('Zamówienie:', {'fields': ('products',)}),
    )

    def save_model(self, request, obj, form, change):

        if 'status' in form.changed_data:
            title = 'Status zamówienia nr '+ str(obj.pk) +' uległ zmianie'
            url = request.build_absolute_uri(reverse('accounts:orders'))
            html_message = render_to_string('cart/status_changed.html', { 'order_id': obj.pk, 'link': url, 'status': obj.get_status_display })
            request.user.email_user(title, '', html_message=html_message)

        super(OrderAdmin, self).save_model(request, obj, form, change)

    # inlines = [
    #     OrderProductInline,
    # ]

class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ('name','price','days')
    list_filter = ('price', 'days')
    search_fields = ['name']

admin.site.register(Order, OrderAdmin)
admin.site.register(ShippingMethod, ShippingMethodAdmin)
